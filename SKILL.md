---
name: prtg
description: Use when working with PRTG Network Monitor via API v2 — querying devices/sensors, creating and editing monitoring objects, building Spectrum-themed dashboards, or exploring network data.
argument-hint: <task description>
allowed-tools: Read, Bash, Write, Edit, Glob, Grep
disable-model-invocation: true
---

# PRTG Network Monitor — API v2 Skill

## Setup

Credentials are stored in a `*.env` file in the working directory. Format:

```
PRTG_HOST=https://your-prtg-server
PRTG_API_KEY=your-api-token
```

**CRITICAL — Windows/Git Bash:** `source file.env` silently fails when the path contains spaces. **Never use bash `source` or `$VAR` substitution for credentials.** Always use Python to load credentials and call APIs:

```python
import subprocess, json, glob

# Load credentials — works regardless of spaces in path
# Sorted + .env.example excluded so selection is deterministic
env_files = sorted(p for p in glob.glob('*.env') if p != '.env.example')
if not env_files:
    raise FileNotFoundError("No *.env file found. Create one with PRTG_HOST and PRTG_API_KEY.")
env = dict(line.strip().split('=', 1) for line in open(env_files[0]) if '=' in line and not line.startswith('#'))
HOST, KEY = env['PRTG_HOST'].rstrip('/'), env['PRTG_API_KEY']

def prtg_get(path):
    r = subprocess.run(
        ['curl', '-s', '-k', f'{HOST}/api/v2/{path}', '-H', f'Authorization: Bearer {KEY}'],
        capture_output=True, text=True, timeout=30)
    if not r.stdout.strip():
        raise RuntimeError(f"Empty response from PRTG (path={path}). stderr: {r.stderr[:200]}")
    return json.loads(r.stdout)

def prtg_request(method, path, body=None):
    """For POST/PATCH/DELETE. Returns parsed JSON, or None for 204 No Content."""
    cmd = ['curl', '-s', '-k', '-X', method.upper(),
           f'{HOST}/api/v2/{path}', '-H', f'Authorization: Bearer {KEY}']
    if body is not None:
        cmd += ['-H', 'Content-Type: application/json', '-d', json.dumps(body)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if not r.stdout.strip():
        return None  # 204 No Content
    return json.loads(r.stdout)

# Example
devices = prtg_get('experimental/devices?limit=3000')
```

Authenticate with: `Authorization: Bearer <api_key>` header. Use `curl -s -k` (allow insecure for internal servers). Base URL: `{host}/api/v2`

## Key References

Read these files on-demand (they are large — only read what you need):

- **`${CLAUDE_SKILL_DIR}/references/api-endpoints.md`** — All endpoint paths, HTTP methods, parameters, and response codes. Read this when you need to know what endpoints exist or their parameters.
- **`${CLAUDE_SKILL_DIR}/references/api-filtering.md`** — Filter syntax, operators, filterable properties, enum values, and common pitfalls. Read this before constructing any `filter=` query.
- **`${CLAUDE_SKILL_DIR}/references/api-schemas.md`** — Request/response body schemas with field names, types, and descriptions. Read this when you need to construct a request body or understand a response.
- **`${CLAUDE_SKILL_DIR}/references/spectrum-design-system.md`** — Compact Spectrum token reference for static visualizations and dashboards.
- **`${CLAUDE_SKILL_DIR}/references/spectrum-full-system.md`** — Full Spectrum component and interaction system for richer UI composition.
- **`${CLAUDE_SKILL_DIR}/references/spectrum-visualization-guidelines.md`** — Decision guide for when to use compact vs full system, plus mandatory branding/look-and-feel rules.
- **`${CLAUDE_SKILL_DIR}/references/visualization-patterns.md`** — Visualization module catalog with v2-first query plans and v1 fallback triggers. Read this for richer dashboards (heatmaps, timeline stacks, SLA bars, flap ranking, dependency views).
- **`${CLAUDE_SKILL_DIR}/references/write-operations-playbook.md`** — Safe write workflow (dry-run planning, approvals, rollback patterns) for `POST/PATCH/DELETE`.
- **`${CLAUDE_SKILL_DIR}/references/error-handling.md`** — HTTP error triage, retry/backoff rules, and v2-to-v1 fallback policy.

## Critical Gotchas & Lessons Learned

1. **Filter syntax is NOT OData.** Use `=`, `!=`, `contains`, `matches` — not `eq`, `ne`. See `references/api-filtering.md` for full reference.
2. **Text values must be double-quoted** in filter expressions: `name = "Ping v2"`, not `name = Ping v2`.
3. **Enum values are bare identifiers:** `status = up`, not `status = "up"`.
4. **`sensor_kind` is not filterable.** You must filter client-side or use `basic.tags contains` as an approximation.
5. **`matches` operator is unreliable** — may return incomplete results. Prefer exact match or `contains`.
6. **Default limit is 100.** Always set `limit=3000` (or appropriate value) to avoid truncated results.
7. **Device status values in responses are prefixed with `SUMMED_INFO_`** (e.g. `SUMMED_INFO_UP`), while sensor statuses are plain (e.g. `UP`). **However, filter expressions always use lowercase without prefix** — `filter=status = down`, NOT `filter=status = SUMMED_INFO_DOWN`.
8. **Path array** on sensors/devices gives the full tree path from root. Extract the parent device with `type == "REFERENCED_DEVICE"`.
9. **The `type` field doesn't exist on individual endpoint responses** (e.g. `/sensors`). It's only available on `/objects`. Sensors have `sensor_kind` instead.
10. **Settings are dynamic and sectioned** — schemas must be fetched from schema endpoints, as they vary by object type. By default, schema and GET endpoints only return the `basic` section. Use `?include=all_sections` to get all available setting sections (e.g. `discoverytypegroup`, `intervalgroup`, `snmpversiongroup`, etc.). You can also include specific sections: `?include=discoverytypegroup,intervalgroup`.
11. **Sensor PATCH uses singular path (bug)** — `PATCH /experimental/sensor/{id}` works, but `PATCH /experimental/sensors/{id}` does not. All other resources use plural consistently. This is a known inconsistency.
12. **Schema endpoint requires a real object ID** — `/experimental/schemas/{id}/patch` needs an actual ID (e.g. `2490`), not a type name.
13. **`parentid` is direct-parent only** — Sensors are children of devices, not groups. To find sensors in a group, first get devices, then query sensors by device IDs.
14. **Experimental sensors have extra fields** — `kind`, `kind_name`, `parent`, `status_since`. Prefer experimental endpoints.
15. **Sensor creation uses `kindid` query param** — `POST /experimental/devices/{id}/sensor?kindid=ping`. The kind goes in the URL, not the body.
16. **POST schema endpoint differs from PATCH schema** — POST uses `GET /experimental/schemas/{parent_id}/post?kind=ping`. PATCH uses `GET /experimental/schemas/{object_id}/patch`.
17. **List endpoints return plain JSON arrays** — `[{...}, {...}]`, NOT `{"items": [...]}`.
18. **IDs are always strings** — `parentid in ["2490","2491"]`, not `parentid in [2490]`.
19. **`parent.id` is NOT filterable** on channels — use `parentid` (flat field).
20. **`parentid = value` requires text** — `parentid = "2490"`, not `parentid = 2490`.
21. **`status_since`** (experimental only) — ISO 8601 timestamp for when current status began.
22. **`last_measurement.display_value`** is numeric — combine with `basic.displayunit` for display.
23. **Timeseries headers are channel IDs, not names** — map via `/experimental/channels?filter=parentid in ["{sensorId}"]`.
24. **`include=all_sections` is needed for full settings** — Schema endpoints (`/experimental/schemas/{id}/patch`) and GET endpoints only return `basic` by default. Add `?include=all_sections` to see all configurable sections. Use `?include=section1,section2` for specific ones.
25. **`discoverytypegroup` = Auto-Discovery settings** — The section name is not intuitive. Key fields: `discoverytype` (`"0"`=off, `"1"`=default, `"2"`=with templates, `"3"`=detailed) and `discoveryschedule` (`"0"`=once, `"1"`=hourly, `"2"`=daily, `"3"`=weekly).
26. **Non-experimental PATCH supports more sections** — `PATCH /devices/{id}` accepts sections like `discoverytypegroup` that may return 501 on the experimental singular endpoint (`/experimental/sensor/{id}`).
27. **`include=sensor_status_summary` for device sensor counts** — By default, device list/read endpoints do NOT return sensor status breakdowns. Add `?include=sensor_status_summary` to get a `sensor_status_summary` object on each device with fields: `calculated_status`, `total`, `down`, `down_acknowledged`, `down_partial`, `warning`, `up`, `paused_by_user`, `paused_by_dependency`, `paused_by_schedule`, `unusual`, `unknown`, `collecting`, etc. Use this to find devices with down sensors without querying sensors separately. You can also use `include=*` as a wildcard for all extra data.

## Endpoint Naming: Plural vs Singular

**Critical:** Endpoint paths vary by resource type — do NOT assume a uniform singular/plural pattern. Check `references/api-endpoints.md` when unsure.

All resource types use **plural** paths for all operations:

| Operation  | Sensors                                          | Devices                              | Groups                               | Probes                               |
|------------|--------------------------------------------------|--------------------------------------|--------------------------------------|--------------------------------------|
| **List**   | `GET /experimental/sensors`                      | `GET /experimental/devices`          | `GET /experimental/groups`           | `GET /experimental/probes`           |
| **Read**   | `GET /experimental/sensors/{id}`                 | `GET /experimental/devices/{id}`     | `GET /experimental/groups/{id}`      | `GET /experimental/probes/{id}`      |
| **Create** | `POST /experimental/devices/{id}/sensor?kindid=` | —                                    | —                                    | —                                    |
| **Edit**   | `PATCH /experimental/sensor/{id}` *(singular!)*  | `PATCH /devices/{id}`                | `PATCH /experimental/groups/{id}`    | —                                    |
| **Delete** | `DELETE /experimental/sensors/{id}`              | `DELETE /experimental/devices/{id}`  | `DELETE /experimental/groups/{id}`   | `DELETE /experimental/probes/{id}`   |

> **Known bug:** Sensor PATCH requires the **singular** path (`/experimental/sensor/{id}`). See gotcha #11.

## Response Format

**List endpoints return plain JSON arrays**, not wrapped objects:

```python
# CORRECT:
data = prtg_get('experimental/sensors?limit=3000')
# data is a list: [{"id": "1002", "name": "Core Health", ...}, ...]

# WRONG — there is no "items" wrapper:
# data.get("items", [])  # This won't work!
```

## Practical API Patterns

### List all devices
```python
devices = prtg_get('experimental/devices?limit=3000')
```

### List sensors filtered by status
```python
import urllib.parse
params = urllib.parse.urlencode({'filter': 'status = down', 'limit': '3000'})
sensors = prtg_get(f'experimental/sensors?{params}')
```

### Find sensors on a specific device
```python
import urllib.parse
params = urllib.parse.urlencode({'filter': 'parentid = "40"', 'limit': '3000'})
sensors = prtg_get(f'experimental/sensors?{params}')
```

### Create a ping sensor on a device
```python
result = prtg_request('POST', f'experimental/devices/{device_id}/sensor?kindid=ping',
                      {"basic": {"name": "My Ping Sensor"}})
```

### Rename a sensor (use singular path — see gotcha #11)
```python
prtg_request('PATCH', f'experimental/sensor/{sensor_id}', {"basic": {"name": "New Name Here"}})
```

### Find sensors in a group (two-step)
```python
import urllib.parse

# Step 1: Get device IDs in the group
params = urllib.parse.urlencode({'filter': 'parentid = "53"', 'limit': '3000'})
devices = prtg_get(f'experimental/devices?{params}')
device_ids = [f'"{d["id"]}"' for d in devices]

# Step 2: Get sensors on those devices
params2 = urllib.parse.urlencode({'filter': f'parentid in [{",".join(device_ids)}]', 'limit': '3000'})
sensors = prtg_get(f'experimental/sensors?{params2}')
```

### Find devices with down sensors
```python
devices = prtg_get('experimental/devices?limit=3000&include=sensor_status_summary')
down_devices = [d for d in devices if d.get('sensor_status_summary', {}).get('down', 0) > 0]
```

### Fetch channel names for timeseries
```python
import urllib.parse
sensor_ids = ["2490", "2491", "2492"]
ids_str = ",".join(f'"{sid}"' for sid in sensor_ids)
params = urllib.parse.urlencode({'filter': f'primary = true and parentid in [{ids_str}]', 'limit': '3000'})
channels = prtg_get(f'experimental/channels?{params}')
channel_map = {str(ch['id']): ch['name'] for ch in channels}
```

### Fetch timeseries data for a sensor
```python
import urllib.parse

sensor_id = "2490"

# Step 1: Get channel IDs for this sensor
params = urllib.parse.urlencode({'filter': f'parentid = "{sensor_id}"', 'limit': '3000'})
channels = prtg_get(f'experimental/channels?{params}')
channel_map = {str(ch['id']): ch['name'] for ch in channels}  # e.g. {"2490.1": "Response Time"}

# Step 2: Fetch timeseries — use type= for predefined windows:
#   live (last 4h), short (last 2d), medium (last 30d), long (last 365d)
# Optionally restrict to specific channels with ?channels=2490.1,2490.2
channel_ids = ",".join(channel_map.keys())
params2 = urllib.parse.urlencode({'channels': channel_ids})
rows = prtg_get(f'experimental/timeseries/{sensor_id}/short?{params2}')

# rows is a list of dicts; each row has a 'datetime' key and channel-ID keys for values:
# [{"datetime": "2024-01-01T00:00:00Z", "2490.1": 12.3, "2490.2": 0.0}, ...]

# Step 3: Remap channel IDs to names for display
named_rows = []
for row in rows:
    named = {"datetime": row["datetime"]}
    for cid, name in channel_map.items():
        if cid in row:
            named[name] = row[cid]
    named_rows.append(named)
```

### Paginate large result sets
```python
import urllib.parse

# Use offset + limit to page through results exceeding 3000
all_devices = []
offset = 0
page_size = 3000
while True:
    params = urllib.parse.urlencode({'limit': page_size, 'offset': offset})
    page = prtg_get(f'experimental/devices?{params}')
    all_devices.extend(page)
    if len(page) < page_size:
        break  # Last page
    offset += page_size
```

## Safe Write Policy (Required)

Before executing any write operation (`POST`, `PATCH`, `DELETE`):

1. Gather object IDs and current values first.
2. Produce a dry-run plan showing endpoint, method, before/after fields, and object count.
3. Require explicit user confirmation before applying writes.
4. Execute writes in small batches.
5. Re-read objects and report final state after completion.

Use `${CLAUDE_SKILL_DIR}/references/write-operations-playbook.md` for full workflow and rollback patterns.

## Visualization / Frontend Guidelines

Support more than dashboards. Valid outputs include status dashboards, timeseries reports, sensor distribution charts, health timelines, topology-like overviews, SLA trend views, and compact NOC wallboard layouts.

Before generating HTML/CSS:

1. Read `${CLAUDE_SKILL_DIR}/references/spectrum-visualization-guidelines.md`.
2. Choose the right system:
   - Use `spectrum-design-system.md` for static/lightweight pages.
   - Use `spectrum-full-system.md` for component-rich, interactive views.

- Link `spectrum.css` (must be in the same directory as generated HTML):
  ```html
  <link rel="stylesheet" href="spectrum.css">
  ```
  Download with: `python3 ${CLAUDE_SKILL_DIR}/scripts/fetch_spectrum.py`
- Use Spectrum design tokens via CSS custom properties (`var(--token-name)`)
- Use semantic color tokens, not hardcoded hex values
- Every visualization MUST include a PRTG-branded top header with:
  - PRTG logo at top-left (inline SVG wordmark or local image asset)
  - visualization title and snapshot timestamp
  - optional context action (for example: "Back to Overview")
- PRTG status → Spectrum color mapping:
  - UP → `fill-color-success` / `background-color-success-soft` (green)
  - DOWN → `fill-color-danger` / `background-color-danger-soft` (red)
  - WARNING → `fill-color-warning` / `background-color-warning-soft` (orange)
  - PAUSED/UNKNOWN → `text-color-disabled` / `background-color-disabled` (grey)
- Font stack: Roboto, "Segoe UI", Tahoma, Arial, Helvetica, Verdana, sans-serif
- Base font size: 14px. Spacing unit: 4px multiples.
- Use card surfaces, consistent spacing rhythm, and clear visual hierarchy (headline, summary KPIs, then details).

### Charts & Timeseries
- Use **Chart.js via CDN** (`chart.js` + `chartjs-adapter-date-fns`). No build step required.
- Chart line colors (Spectrum 60-level palette): blue-60 `#0F67FF`, green-60 `#A4AD19`, dark-orange-60 `#DE6800`, cyan-60 `#0097B2`, purple-60 `#8A3FFC`, magenta-60 `#D12771`
- Grid lines: `#F1F1F3`. Font: Roboto.
- **Always label channels by name** (e.g. "Response Time"), not by channel ID (e.g. "2490.0"). Map `channel_id → name` via the channels endpoint before rendering.
- When rendering charts in expandable/hidden containers: wrap each `<canvas>` in a fixed-height `<div>` with `overflow: hidden; position: relative`. Create charts with `requestAnimationFrame` after the container becomes visible.

### Visualization Presets (v2 First)

When a user asks for "more visuals", pick one preset and compose modules from `references/visualization-patterns.md`:

- `exec-view`: status heatmap + blast radius + top incident list
- `ops-view`: 24h status timeline + flapping leaderboard + capacity forecast
- `security-view`: SSL expiry tiers + vulnerable endpoints + cert trend

For each module:

1. List the exact endpoints used.
2. State data source as `v2` or `v1-fallback`.
3. Keep color/status mapping Spectrum-compliant.

### API v1 Fallback Policy

- Default to API v2 for all reads/writes.
- Use API v1 only when v2 cannot serve the required visualization (for example endpoint `404/501` or missing required fields).
- If any module uses v1, explicitly disclose it in output.
- Do not switch the whole task to v1 if only one module needs fallback.

Minimal fallback pattern:

```python
import subprocess, json

def prtg_get_v1(path):
    # Uses the same token, but v1 expects query params.
    r = subprocess.run(
        ['curl', '-s', '-k', f'{HOST}/api/{path}&apitoken={KEY}'],
        capture_output=True, text=True, timeout=30)
    if not r.stdout.strip():
        raise RuntimeError(f"Empty v1 response (path={path})")
    return json.loads(r.stdout)
```

Common v1 fallback endpoints for visuals:

- Object tables: `table.json?content=sensors|devices|groups&output=json`
- Historic series: `historicdata.json?id=<sensorid>&avg=<seconds>&sdate=<start>&edate=<end>`

## Bundled Assets & Fixture Mode

- Dashboard templates:
  - `${CLAUDE_SKILL_DIR}/assets/dashboard-templates/status-overview-template.html`
  - `${CLAUDE_SKILL_DIR}/assets/dashboard-templates/timeseries-template.html`
- Offline fixtures:
  - `${CLAUDE_SKILL_DIR}/assets/fixtures/devices.sample.json`
  - `${CLAUDE_SKILL_DIR}/assets/fixtures/sensors.sample.json`
  - `${CLAUDE_SKILL_DIR}/assets/fixtures/channels.sample.json`
  - `${CLAUDE_SKILL_DIR}/assets/fixtures/timeseries.sample.json`

When a live server is unavailable, use fixture mode to produce deterministic demo output:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/build_fixture_dashboard.py" --output fixture-dashboard.html
```

## Compatibility Notes

- Runtime placeholders:
  - `${CLAUDE_SKILL_DIR}` resolves to the installed skill directory.
  - `$ARGUMENTS` resolves to the user task text.
- For Codex-style environments where those placeholders are unavailable, resolve paths relative to the repository root and pass task text directly in the user prompt.
- Keep scripts Python-first for Windows path safety (avoid shell `source` semantics).

## Scripts

- **`${CLAUDE_SKILL_DIR}/scripts/update_docs.py`** — Refresh API docs from the live PRTG server. Run from your working directory (where the `*.env` file is). Outputs to `docs/` and `prtg_api_resolved.yaml` in the CWD.
  ```bash
  python3 "${CLAUDE_SKILL_DIR}/scripts/update_docs.py"
  ```
- **`${CLAUDE_SKILL_DIR}/scripts/fetch_spectrum.py`** — Download `spectrum.css` from your PRTG server. Run from your working directory.
  ```bash
  python3 "${CLAUDE_SKILL_DIR}/scripts/fetch_spectrum.py"
  ```
- **`${CLAUDE_SKILL_DIR}/scripts/preflight.py`** — Verify credentials, v2 connectivity, filter syntax behavior, optional v1 fallback reachability, and local `spectrum.css` presence.
  ```bash
  python3 "${CLAUDE_SKILL_DIR}/scripts/preflight.py"
  ```
- **`${CLAUDE_SKILL_DIR}/scripts/build_fixture_dashboard.py`** — Build an offline HTML dashboard from local fixture JSON files.
  ```bash
  python3 "${CLAUDE_SKILL_DIR}/scripts/build_fixture_dashboard.py" --output fixture-dashboard.html
  ```
- **`${CLAUDE_SKILL_DIR}/scripts/validate_skill.py`** — Validate frontmatter, file references, and required repository assets.
  ```bash
  python3 "${CLAUDE_SKILL_DIR}/scripts/validate_skill.py"
  ```
- **`${CLAUDE_SKILL_DIR}/scripts/prtg_client.py`** — Shared helper client for pagination, v1 fallback reads, and safe credential handling. Import from custom scripts instead of rewriting API glue.

---

## Task

$ARGUMENTS
