#!/usr/bin/env python3
"""
update_docs.py — Refresh PRTG API docs from live server spec.

Usage:
    python3 update_docs.py [credentials_file]

If no credentials file is given, the script auto-detects any *.env file in
the current directory that contains PRTG_HOST and PRTG_API_KEY variables.

What it does:
    1. Reads host + API key from credentials file
    2. Downloads prtg.api.yaml from {host}/api/v2/oas/
    3. Downloads all externally referenced YAML files
    4. Resolves all $ref pointers into a single flat spec
    5. Saves the resolved spec as prtg_api_resolved.yaml
    6. Regenerates docs/api-endpoints.md and docs/api-schemas.md
    7. Prints a changelog: added/removed/changed endpoints and schemas

Output files are written to the current working directory (where you run
the script from), not the script's own directory.
"""

import sys
import os
import re
import json
import tempfile
import shutil
import urllib.request
import urllib.error
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Dependency check
# ---------------------------------------------------------------------------

def ensure_deps():
    try:
        import yaml
        import jsonref
        import dotenv
    except ImportError as e:
        missing = str(e).split("'")[1]
        pkg = {"yaml": "pyyaml", "jsonref": "jsonref", "dotenv": "python-dotenv"}.get(missing, missing)
        print(f"Missing dependency: {missing}. Installing {pkg}...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

ensure_deps()

import yaml
import jsonref
from dotenv import dotenv_values

# ---------------------------------------------------------------------------
# Credentials
# ---------------------------------------------------------------------------

# CWD is the user's working directory (where they run the script from).
# The *.env file with PRTG_HOST and PRTG_API_KEY should be there.
CWD = Path.cwd()

def load_credentials(cred_file=None):
    if cred_file:
        candidates = [Path(cred_file)]
    else:
        candidates = sorted(CWD.glob("*.env"))
        # Skip the example template
        candidates = [p for p in candidates if p.name != ".env.example"]

    for path in candidates:
        try:
            cfg = dotenv_values(path)
        except Exception:
            continue
        host = cfg.get("PRTG_HOST", "").strip().rstrip("/")
        key  = cfg.get("PRTG_API_KEY", "").strip()
        if host and key:
            print(f"Using credentials: {path.name}  ->  {host}")
            return host, key

    sys.exit("No credentials file found. Expected a *.env file with PRTG_HOST and PRTG_API_KEY.")

# ---------------------------------------------------------------------------
# Download helpers
# ---------------------------------------------------------------------------

def http_get(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    # Disable SSL verification (internal servers)
    import ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, context=ctx) as resp:
        return resp.read().decode("utf-8")

def yaml_loader_factory(base_dir, host, api_key):
    """Returns a loader that resolves relative file:// refs from the temp dir."""
    import ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    def loader(uri):
        # Convert file:// URIs to local paths
        if uri.startswith("file://"):
            local = urllib.request.url2pathname(uri[7:])
            with open(local, encoding="utf-8") as f:
                return yaml.safe_load(f)
        with urllib.request.urlopen(uri, context=ctx) as resp:
            return yaml.safe_load(resp.read().decode("utf-8"))

    return loader

# ---------------------------------------------------------------------------
# Fetch and resolve spec
# ---------------------------------------------------------------------------

def fetch_and_resolve(host, api_key):
    oas_base_url = f"{host}/api/v2/oas/"
    print(f"\nFetching spec from {oas_base_url}prtg.api.yaml ...")

    main_yaml_text = http_get(oas_base_url + "prtg.api.yaml")
    main_dict = yaml.safe_load(main_yaml_text)

    # Find all external $ref files
    external_files = sorted(set(
        ref.split("#")[0]
        for ref in re.findall(r'\$ref:\s*["\']?([^"\'\n]+)["\']?', main_yaml_text)
        if not ref.startswith("#")
    ))
    print(f"Downloading {len(external_files)} referenced component files...")

    # Write everything into a temp directory
    tmpdir = Path(tempfile.mkdtemp(prefix="prtg_oas_"))
    try:
        main_file = tmpdir / "prtg.api.yaml"
        main_file.write_text(main_yaml_text, encoding="utf-8")

        failed = []
        for rel_path in external_files:
            url = oas_base_url + rel_path
            dest = tmpdir / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            try:
                content = http_get(url)
                dest.write_text(content, encoding="utf-8")
            except Exception as e:
                failed.append((rel_path, str(e)))

        if failed:
            print(f"  WARNING: {len(failed)} files failed to download:")
            for f, e in failed:
                print(f"    {f}: {e}")

        # Resolve all $refs
        print("Resolving $ref pointers...")
        base_uri = main_file.as_uri()
        loader = yaml_loader_factory(tmpdir, host, api_key)
        spec_with_refs = jsonref.replace_refs(
            yaml.safe_load(main_file.read_text(encoding="utf-8")),
            base_uri=base_uri,
            loader=loader,
            lazy_load=False,
        )
        resolved = json.loads(jsonref.dumps(spec_with_refs))
        print(f"  Resolved: {len(resolved.get('paths', {}))} paths, "
              f"{len(resolved.get('components', {}).get('schemas', {}))} schemas")
        return resolved
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

# ---------------------------------------------------------------------------
# Changelog diff
# ---------------------------------------------------------------------------

def compute_changelog(old_spec, new_spec):
    old_paths = set(old_spec.get("paths", {}).keys())
    new_paths = set(new_spec.get("paths", {}).keys())

    added_paths   = new_paths - old_paths
    removed_paths = old_paths - new_paths
    common_paths  = old_paths & new_paths

    changed_ops = []
    for path in sorted(common_paths):
        old_obj = old_spec["paths"][path]
        new_obj = new_spec["paths"][path]
        for method in set(list(old_obj.keys()) + list(new_obj.keys())):
            if method not in ("get","post","put","patch","delete"): continue
            old_op = old_obj.get(method)
            new_op = new_obj.get(method)
            if old_op is None or new_op is None:
                changed_ops.append((path, method.upper(), "added" if old_op is None else "removed"))
            elif json.dumps(old_op, sort_keys=True) != json.dumps(new_op, sort_keys=True):
                changed_ops.append((path, method.upper(), "changed"))

    old_schemas = set(old_spec.get("components", {}).get("schemas", {}).keys())
    new_schemas = set(new_spec.get("components", {}).get("schemas", {}).keys())

    return {
        "added_paths":   sorted(added_paths),
        "removed_paths": sorted(removed_paths),
        "changed_ops":   changed_ops,
        "added_schemas":   sorted(new_schemas - old_schemas),
        "removed_schemas": sorted(old_schemas - new_schemas),
    }

def print_changelog(cl):
    total_changes = (len(cl["added_paths"]) + len(cl["removed_paths"]) +
                     len(cl["changed_ops"]) + len(cl["added_schemas"]) +
                     len(cl["removed_schemas"]))

    print("\n" + "=" * 60)
    print("CHANGELOG")
    print("=" * 60)

    if not total_changes:
        print("No changes detected.")
        return

    if cl["added_paths"]:
        print(f"\nNew endpoints ({len(cl['added_paths'])}):")
        for p in cl["added_paths"]: print(f"  + {p}")

    if cl["removed_paths"]:
        print(f"\nRemoved endpoints ({len(cl['removed_paths'])}):")
        for p in cl["removed_paths"]: print(f"  - {p}")

    if cl["added_schemas"]:
        print(f"\nNew schemas ({len(cl['added_schemas'])}):")
        for s in cl["added_schemas"]: print(f"  + {s}")

    if cl["removed_schemas"]:
        print(f"\nRemoved schemas ({len(cl['removed_schemas'])}):")
        for s in cl["removed_schemas"]: print(f"  - {s}")

    changed_only = [(p, m, k) for p, m, k in cl["changed_ops"] if k == "changed"]
    if changed_only:
        print(f"\nModified operations ({len(changed_only)}):")
        for path, method, _ in changed_only:
            print(f"  ~ {method} {path}")

    print()

# ---------------------------------------------------------------------------
# Tag classification
# ---------------------------------------------------------------------------

TAG_ORDER = [
    "Sensors", "Devices", "Channels", "Groups", "Probes",
    "Timeseries", "Objects", "Schemas", "Accounts",
    "Libraries", "Lookups", "Authentication", "System",
]

def get_tag(path, op):
    tags = op.get("tags", [])
    if tags: return tags[0]
    if "/sensor"  in path: return "Sensors"
    if "/device"  in path: return "Devices"
    if "/channel" in path: return "Channels"
    if "/group"   in path: return "Groups"
    if "/probe"   in path: return "Probes"
    if "/timeseries" in path: return "Timeseries"
    if "/object"  in path: return "Objects"
    if "/schema"  in path: return "Schemas"
    if "/user" in path or "/account" in path or "/apikey" in path: return "Accounts"
    if "/librar"  in path: return "Libraries"
    if "/lookup"  in path: return "Lookups"
    if "/auth" in path or "/login" in path or "/token" in path: return "Authentication"
    return "System"

def endpoint_flags(path, op):
    parts = []
    if "/experimental/" in path: parts.append("[E]")
    if op.get("deprecated"):     parts.append("[D]")
    return (" " + " ".join(parts)) if parts else ""

def grouped_ops(spec):
    groups = defaultdict(list)
    for path, path_obj in sorted(spec.get("paths", {}).items()):
        for method in ["get", "post", "put", "patch", "delete"]:
            if method not in path_obj: continue
            op = path_obj[method]
            tag = get_tag(path, op)
            groups[tag].append((path, method.upper(), op))
    return groups

# ---------------------------------------------------------------------------
# Schema helpers
# ---------------------------------------------------------------------------

def prop_type_str(schema, depth=0):
    if not schema or depth > 3: return "any"
    if "$ref" in schema: return schema["$ref"].split("/")[-1]
    t     = schema.get("type", "")
    enum  = schema.get("enum")
    if enum:
        vals = ", ".join(repr(str(v)) for v in enum[:8])
        if len(enum) > 8: vals += f", ... ({len(enum)} values)"
        return f"enum: [{vals}]"
    if t == "array":
        return f"array of {prop_type_str(schema.get('items', {}), depth+1)}"
    if t == "object": return "object"
    fmt = schema.get("format", "")
    if t == "string" and fmt: return f"string ({fmt})"
    return t or "any"

def flatten_schema(schema, prefix="", depth=0, rows=None):
    if rows is None: rows = []
    if not schema or depth > 4: return rows
    t     = schema.get("type", "")
    props = schema.get("properties", {})
    required_fields = schema.get("required", [])
    if t == "array":
        flatten_schema(schema.get("items", {}), prefix, depth, rows)
        return rows
    for name, prop in (props or {}).items():
        full_name = f"{prefix}.{name}" if prefix else name
        ptype = prop_type_str(prop)
        req   = "Yes" if name in required_fields else ""
        desc  = prop.get("description", "").replace("\n", " ").strip()
        if len(desc) > 140: desc = desc[:137] + "..."
        rows.append((full_name, ptype, req, desc))
        if prop.get("type") == "object" and prop.get("properties") and depth < 2:
            flatten_schema(prop, full_name, depth+1, rows)
        elif (prop.get("type") == "array"
              and prop.get("items", {}).get("type") == "object"
              and depth < 1):
            flatten_schema(prop.get("items", {}), full_name, depth+1, rows)
    return rows

def get_body_schema(op_part):
    """Returns (schema, mime) from requestBody or response content."""
    content = op_part.get("content", {}) if op_part else {}
    for mime, media in content.items():
        return media.get("schema", {}), mime
    return None, None

# ---------------------------------------------------------------------------
# Generate api-endpoints.md
# ---------------------------------------------------------------------------

def gen_endpoints(spec):
    groups = grouped_ops(spec)
    tag_counts = {t: len(groups.get(t, [])) for t in TAG_ORDER}
    total = sum(tag_counts.values())
    num_paths = len(spec.get("paths", {}))

    lines = [
        "# PRTG API v2 — Endpoint Reference",
        "",
        f"Auto-generated from current PRTG server spec. {total} operations across {num_paths} paths.",
        "",
        "**Legend:** [D] = Deprecated, [E] = Experimental",
        "",
        "## Contents",
        "",
    ]
    for t in TAG_ORDER:
        cnt = tag_counts.get(t, 0)
        if cnt:
            lines.append(f"- [{t}](#{t.lower()}) ({cnt} endpoints)")
    lines.append("")

    for tag in TAG_ORDER:
        ops = groups.get(tag, [])
        if not ops: continue
        lines += [f"## {tag}", ""]
        for path, method, op in ops:
            f = endpoint_flags(path, op)
            summary = op.get("summary", op.get("description", ""))
            summary = summary.strip().split("\n")[0] if summary else ""

            lines.append(f"### `{method} {path}`{f}")
            lines.append("")
            if summary:
                lines += [summary, ""]

            # Parameters
            params = op.get("parameters", [])
            if params:
                lines += [
                    "**Parameters:**", "",
                    "| Name | In | Type | Required | Default | Description |",
                    "|------|----|------|----------|---------|-------------|",
                ]
                for p in params:
                    schema  = p.get("schema", {})
                    default = str(schema.get("default", "")) if "default" in schema else ""
                    desc    = p.get("description", "").replace("\n", " ").strip()
                    if len(desc) > 110: desc = desc[:107] + "..."
                    lines.append(
                        f"| `{p.get('name','')}` | {p.get('in','')} "
                        f"| {prop_type_str(schema)} "
                        f"| {'Yes' if p.get('required') else ''} "
                        f"| {default} | {desc} |"
                    )
                lines.append("")

            # Request body
            rb_schema, rb_mime = get_body_schema(op.get("requestBody", {}))
            if rb_schema is not None:
                lines += [f"**Request body** ({rb_mime}): {prop_type_str(rb_schema)}", ""]

            # Responses
            responses = op.get("responses", {})
            if responses:
                lines += ["**Responses:**", ""]
                for code, resp in responses.items():
                    resp_schema, _ = get_body_schema(resp)
                    extra = f" — {prop_type_str(resp_schema)} (see schema)" if resp_schema else ""
                    lines.append(f"- `{code}`: {resp.get('description', '')}{extra}")
                lines.append("")

            lines += ["---", ""]

    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Generate api-schemas.md
# ---------------------------------------------------------------------------

def gen_schemas(spec):
    groups = grouped_ops(spec)

    lines = [
        "# PRTG API v2 — Schema Reference",
        "",
        "Auto-generated from current PRTG server spec. Contains request/response body schemas.",
        "",
        "## Contents",
        "",
    ]
    for t in TAG_ORDER:
        if groups.get(t):
            lines.append(f"- [{t}](#{t.lower()})")
    lines.append("")

    for tag in TAG_ORDER:
        ops = groups.get(tag, [])
        if not ops: continue
        lines += [f"## {tag}", ""]

        for path, method, op in ops:
            f = endpoint_flags(path, op)
            summary = op.get("summary", "").strip().split("\n")[0]
            lines.append(f"### `{method} {path}`{f}")
            lines.append("")
            if summary:
                lines += [f"_{summary}_", ""]

            has_content = False

            # Request body
            rb_schema, rb_mime = get_body_schema(op.get("requestBody", {}))
            if rb_schema is not None:
                has_content = True
                lines += [f"**Request Body:** {rb_schema.get('type', 'object')}", ""]
                rows = flatten_schema(rb_schema)
                if rows:
                    lines += [
                        "| Property | Type | Required | Description |",
                        "|----------|------|----------|-------------|",
                    ]
                    for name, ptype, req, desc in rows:
                        lines.append(f"| `{name}` | {ptype} | {req} | {desc} |")
                    lines.append("")

            # Success responses
            for code in ["200", "201", "204"]:
                resp = op.get("responses", {}).get(code)
                if resp is None: continue
                has_content = True
                if code == "204":
                    lines += [f"**Response `{code}`:** No content.", ""]
                    continue
                resp_schema, _ = get_body_schema(resp)
                if resp_schema is None: continue
                is_array = resp_schema.get("type") == "array"
                actual   = resp_schema.get("items", resp_schema) if is_array else resp_schema
                label    = " (array item)" if is_array else ""
                lines += [f"**Response `{code}`{label}:**", ""]
                rows = flatten_schema(actual)
                if rows:
                    lines += [
                        "| Property | Type | Required | Description |",
                        "|----------|------|----------|-------------|",
                    ]
                    for name, ptype, req, desc in rows:
                        lines.append(f"| `{name}` | {ptype} | {req} | {desc} |")
                    lines.append("")
                else:
                    lines += [f"_{actual.get('type','object')} (no properties documented)_", ""]

            if not has_content:
                lines += ["_No request/response body._", ""]

            lines += ["---", ""]

    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    cred_file = sys.argv[1] if len(sys.argv) > 1 else None
    host, api_key = load_credentials(cred_file)

    docs_dir     = CWD / "docs"
    resolved_out = CWD / "prtg_api_resolved.yaml"
    endpoints_out = docs_dir / "api-endpoints.md"
    schemas_out   = docs_dir / "api-schemas.md"

    docs_dir.mkdir(exist_ok=True)

    # Load old spec for diffing (if it exists)
    old_spec = {}
    if resolved_out.exists():
        print(f"\nLoading previous spec for diff: {resolved_out.name}")
        with open(resolved_out, encoding="utf-8") as f:
            old_spec = yaml.safe_load(f) or {}

    # Fetch and resolve new spec
    new_spec = fetch_and_resolve(host, api_key)

    # Diff
    if old_spec:
        changelog = compute_changelog(old_spec, new_spec)
    else:
        changelog = None

    # Save resolved YAML
    print(f"\nSaving resolved spec -> {resolved_out.name}")
    with open(resolved_out, "w", encoding="utf-8") as f:
        yaml.dump(new_spec, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    # Generate docs
    print(f"Generating {endpoints_out.name} ...")
    endpoints_out.write_text(gen_endpoints(new_spec), encoding="utf-8")

    print(f"Generating {schemas_out.name} ...")
    schemas_out.write_text(gen_schemas(new_spec), encoding="utf-8")

    print("Done.")

    # Print changelog last so it's prominent
    if changelog:
        print_changelog(changelog)
    else:
        print("\n(No previous spec to diff against — changelog skipped.)")

if __name__ == "__main__":
    main()
