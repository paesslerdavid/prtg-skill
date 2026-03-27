# PRTG API v2 — Sensor Creation Guide

Hard-won knowledge from automating creation of 186 sensor kinds across 132 devices.
All findings are from `dev-dk-007.paeqa.int:1615` running PRTG API v2 (experimental).

---

## Complete Creation Workflow

```
1. List creatable kinds on a device
   GET /experimental/schemas/{deviceId}?limit=1000
   → filter to creatable=true entries

2. Get full POST schema for the chosen kind
   GET /experimental/schemas/{deviceId}/post?kind={kind}&include=all_sections
   → schema at components.schemas.modifyItemSchema

3. If HasMetaScan in flags → run metascan
   POST /experimental/devices/{deviceId}/metascan?kind={kind}
   Body: {} or {"params": {...}} for credential overrides

4. Build POST body from schema + metascan result + any known settings

5. Create the sensor
   POST /experimental/devices/{deviceId}/sensor?kindid={kind}
   Body: {section: {field: value}, ...}
```

---

## Critical Parameter / Endpoint Quirks

### `kindid` vs `kind` — inconsistent across endpoints

| Endpoint | Parameter name |
|----------|---------------|
| `POST /experimental/devices/{id}/sensor` | `?kindid=ping` |
| `POST /experimental/devices/{id}/metascan` | `?kind=ping` |
| `GET /experimental/schemas/{id}/post` | `?kind=ping` |
| `GET /experimental/schemas/{id}` (list) | N/A — kind is in the response body |

Always use `kindid` for sensor creation, `kind` everywhere else.

### Schema list truncates at 100 — always pass `limit=1000`

```python
# WRONG — silently returns only ~100 of ~329 sensor kinds
kinds = client.get(f'experimental/schemas/{device_id}')

# CORRECT
kinds = client.get(f'experimental/schemas/{device_id}', params={'limit': '1000'})
```

### POST schema requires `include=all_sections`

Without this flag, required fields from non-basic sections are omitted from the schema response, making it impossible to build a valid request body.

```python
schema = client.get(
    f'experimental/schemas/{device_id}/post',
    params={'kind': kind_id, 'include': 'all_sections'}
)
modify = schema['components']['schemas']['modifyItemSchema']
```

### Deprecated schema endpoint — never use

```python
# WRONG — deprecated, do not use
GET /schemas/{kind}

# CORRECT
GET /experimental/schemas/{deviceId}/post?kind={kind}&include=all_sections
```

---

## Kind ID Version Suffixes

Sensor kind IDs may include a numeric version suffix reflecting the schema version on the target device:
- `paessler.snmp.cpu_usage_sensor.65`
- `paessler.ssh.disk_free_sensor.22`
- `paessler.AWS.alarm_sensor.79`

**Always strip trailing `.\d+` when comparing kinds** to avoid false "not found" results and accidental duplicates.

```python
import re
def strip_version(kind_id: str) -> str:
    return re.sub(r'\.\d+$', '', kind_id)

# strip_version("paessler.snmp.cpu_usage_sensor.65") == "paessler.snmp.cpu_usage_sensor"
```

The schema list endpoint returns the unversioned kind ID in its `kind` field. The `POST /sensor?kindid=` endpoint accepts either form.

---

## Building the POST Body

### Sections to skip

The following sections appear in GET schemas but must NOT be sent in POST requests (they are server-managed or cause 400 errors):

```python
SKIP_SECTIONS = {
    "scheduledependency", "AccessGroup", "comment", "coverage", "debug",
    "downtimetotal", "favorite", "fixed", "href", "id", "kind", "kind_name",
    "lastdown", "lastup", "message", "name", "parent", "performance_impact",
    "status", "status_since", "type", "uptimetotal", "intervalgroup",
    "channelgroup",
}
```

### Filling required fields

Walk `modifyItemSchema.properties` for each section, then for each field:

```python
for field_name, field_def in section_def['properties'].items():
    if field_name == '_inherited':
        continue  # Handle separately — see _inherited bug below
    meta = field_def.get('x-prtg-meta', {})
    if meta.get('required'):
        if 'default' in field_def:
            body[section][field_name] = field_def['default']
        elif field_def.get('type') == 'integer':
            pass  # Do NOT fill "" — server rejects type mismatches.
                  # Leave out and rely on error message to find valid range.
        else:
            body[section][field_name] = ""  # Will fail, but gives a clear error
```

### Sensors without `basic.name`

Metascan-based sensors often do NOT accept `basic.name` in the POST body. The sensor name is derived from the metascan selection (e.g. "Disk Free: /"). Before including `name`, verify the POST schema has `name` in the `basic` section properties.

### POST schema field names differ from UI labels

The API field name is **not** the UI label. Always check the POST schema for exact names.

Example: "Channel Name" in the UI is `oidgroup.channel`, not `oidgroup.channelname`. The API rejects unknown field names outright (`BAD_REQUEST: unknown field`).

---

## Metascan

### Basic call

```python
# Must be POST. Must have at least an empty JSON body.
result = client.request('POST', f'experimental/devices/{device_id}/metascan?kind={kind}', {})
# Returns: list of discovered items, or error dict
```

- `GET` on the metascan endpoint → `404`
- `POST` with no body (not even `{}`) → `400 EOF`
- Calling metascan on a kind without `HasMetaScan` flag → `400: sensor kind does not support metascan`

### Credential params (undocumented `{"params": ...}` wrapper)

For sensor kinds that need per-sensor credentials (e.g. NetApp legacy, SSH with custom params), the metascan body must wrap credentials in a `"params"` key:

```python
# Without params — works for most sensors
body = {}

# With credential params (NetApp legacy, etc.)
body = {
    "params": {
        "username": "admin",
        "password": "secret",
        "host": "192.168.1.1"
    }
}
result = client.request('POST', f'experimental/devices/{device_id}/metascan?kind={kind}', body)
```

The schema's `metascan_body` field documents what keys are accepted in `params`. This wrapper is not mentioned in the official API docs.

### Using metascan results in the POST body

The `metascan_field` ref in `additionalProperties.properties.metascan.x-prtg-meta` encodes the target section and key using a JSON pointer path:

```
metascan_field: "#/components/schemas/modifyItemSchema/properties/diskfree/properties/disk"
```

Parse out section (`diskfree`) and key (`disk`):

```python
# metascan_field path: .../properties/{section}/properties/{key}
parts = metascan_ref.split('/')
section_name = parts[5]   # e.g. "diskfree"
key_field = parts[6]       # NOT parts[-1], path ends at the key name itself
                            # Actually the format is .../properties/{section}/disk
                            # Check create_sensors.py for the exact split logic

# Collect all values from metascan results for that key
key_values = [item[key_field] for item in metascan_data if key_field in item]
body[section_name] = {key_field: key_values}
```

### Legacy sensors — `{"params": {...}}` body format

Some older (v1) sensors use a different body format where the metascan selection is wrapped:

```python
# v2 sensors: flat field in a section
body = {"diskfree": {"disk": ["C:", "D:"]}}

# Legacy sensors (e.g. NetApp aggregate, I/O, etc.): params wrapper
body = {"params": {"aggregate": "aggr0"}}
```

Check the metascan response structure to determine which format is needed.

### Parallelizing metascans

Metascans are slow (up to 15s each). Run 5 concurrently per device using `ThreadPoolExecutor`:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

METASCAN_PARALLEL = 5

def prefetch_metascans(device_id, sensors_needing_metascan):
    """sensors_needing_metascan: list of (kind_id, sensor_name) tuples"""
    cache = {}
    with ThreadPoolExecutor(max_workers=METASCAN_PARALLEL) as pool:
        futures = {
            pool.submit(run_metascan, device_id, kind_id): kind_id
            for kind_id, _ in sensors_needing_metascan
        }
        for future in as_completed(futures):
            kind_id = futures[future]
            cache[kind_id] = future.result()  # (data, error)
    return cache
```

---

## Known API Bugs and Workarounds

### Bug 1: `_inherited` NULL rejected on POST

**Affected kinds:** `sshscript`, `sshscriptxml`, `snmpciscoasavpnconnections`, `snmpciscoasavpnusers`

The POST schema shows `_inherited` with `default: true` but the server rejects it as NULL if omitted. You must explicitly set `_inherited: true` in the POST body for sections like `scriptplaceholdergroup` and `snmpversiongroup`.

```python
# Workaround
body["scriptplaceholdergroup"] = {"_inherited": True}
```

**Note:** For `snmpciscoasavpnconnections` and `snmpciscoasavpnusers`, even explicit `_inherited: true` is rejected (`snmpversiongroup._inherited is invalid: the NULL value is not allowed`). These sensors cannot currently be created via API v2.

### Bug 2: Disabled channels still validated as required

**Affected kind:** `snmpcustomadvanced`

Setting `usechannel{N}: "0"` does NOT suppress validation of that channel's fields. Channels 2–10 have `channel{N}name` marked as `required: true` in the POST schema, and the server enforces this even when the channel is explicitly disabled.

```python
# WRONG — fails with "channel2name is required" etc.
body = {
    "oidgroup": {
        "channel1name": "sysUpTime",
        "channel1oid": "1.3.6.1.2.1.1.3.0",
        "usechannel2": "0",
        # ... more disabled channels
    }
}

# CORRECT workaround — provide placeholder names + explicit unit for all 10 channels
body = {
    "oidgroup": {
        "channel1name": "sysUpTime",
        "channel1oid": "1.3.6.1.2.1.1.3.0",
        "channel1unit": "Count",
        "usechannel2": "0", "channel2name": "Channel 2", "channel2unit": "Count",
        "usechannel3": "0", "channel3name": "Channel 3", "channel3unit": "Count",
        # ... repeat for channels 4-10
    }
}
```

Also note: `unit` must be set explicitly to `"Count"` (or any valid value) — without it, `channel{N}valuelookup` is validated against `setting-lookups/valuelookups`, which is fine (261 results), but `unit` must be present to bypass it.

### Bug 3: `snmpcustomlookup` — lookup validation broken

**Affected kind:** `snmpcustomlookup`

The POST schema declares `oidgroup.lookups` with `lookupkey: "lookups"`, but `GET /setting-lookups/lookups` returns 404. The values actually come from metascan, but `additionalProperties` has no `metascan_field` declaration. Result: validation fails unconditionally for any value provided.

```
GET /setting-lookups/lookups → 404 "lookup not found: lookups"
POST with metascan value → BAD_REQUEST "no lookup validation possible for lookup lookups"
```

**Status:** Cannot be created via API v2. Bug filed.

### Bug 4: Integer fields without defaults

Many sensor kinds have required integer fields with no default and no range in the schema. The server only reveals the valid range in the error message after a failed submission.

Known affected fields:

| Kind | Field | Valid range (from error) |
|------|-------|--------------------------|
| `port` | `portadvanced.allowedcode` | 100–599 |
| `httppushdata` | `pushdata.timethreshold` | ≥1 |
| `imap` | `behavior.contentwarningtimevalue` | ≥1 |
| `ssl`, `sslcertificate` | `connectionspecific.socksproxyport` | 1–65535 |
| `ipfixheader`, `netflowheader`, `jflowheader` | `flowspecific.flowtimeout` | ≥1 |
| `ipfixheader`, `netflowheader`, `jflowheader` | `flowspecific.port` | 1–65535 |

Strategy: omit integer fields without defaults → get a clear error → retry with the correct value from the error message.

### Bug 5: Unknown metascan ID for AWS sensors (schema version .79)

**Affected kinds:** `paessler.AWS.alarm_sensor`, `paessler.AWS.ebs_sensor`, `paessler.AWS.ec2_sensor`, `paessler.AWS.elb_sensor`, `paessler.AWS.rds_sensor`

The metascan endpoint internally resolves the unversioned kind to `paessler.AWS.alarm_sensor.79`, then fails because no metascan handler is registered for that versioned ID. Non-metascan AWS sensors (e.g. AWS Cost) work fine.

```
POST /experimental/devices/19833/metascan?kind=paessler.AWS.alarm_sensor
→ BAD_REQUEST: "unknown metascanId: paessler.AWS.alarm_sensor.79"
```

**Status:** Cannot be created via API v2. Bug filed.

### Bug 6: Metascan timeout regression

~47 sensor kinds cause `POST /metascan` to hang indefinitely (no response within 15s). Set a timeout and treat these as temporarily blocked. This is a known regression in dev builds; check if fixed in newer PRTG versions.

---

## Resume / Duplicate Detection

When re-running creation scripts, detect already-created sensors by **kind ID** (not name). Metascan-based sensors get names from their discovery data (e.g. "Disk Free: /" instead of "SNMP Disk Free"), making name-based deduplication unreliable.

```python
import re

def get_existing_kind_ids(client, device_id):
    """Fetch all sensor kind IDs on a device, with version suffixes stripped."""
    sensors = client.get('experimental/sensors', params={
        'filter': f'parentid = "{device_id}"',
        'limit': '3000'
    })
    return {re.sub(r'\.\d+$', '', s.get('kind', '')) for s in sensors}

# Before creating:
existing = get_existing_kind_ids(client, device_id)
if strip_version(kind_id) in existing:
    print(f"  Skipping {kind_id} — already exists")
    continue
```

For group-level deduplication (one running instance per kind across the whole group):

```python
# Get all sensors in all devices in the group
all_sensors = client.get('experimental/sensors', params={
    'filter': f'parentid in [{",".join(f'"{did}"' for did in device_ids)}]',
    'limit': '3000'
})
kind_to_sensors = {}
for s in all_sensors:
    base_kind = re.sub(r'\.\d+$', '', s.get('kind', ''))
    kind_to_sensors.setdefault(base_kind, []).append(s)

# Deduplication priority: UP > WARNING > DOWN, prefer Confluence-specified device
```

---

## Sensor Creatability Hints

The kind listing returns `hints` when `creatable: false`:

| Hint | Meaning |
|------|---------|
| `CredentialsMissing` | Device has the credential group configured but it's empty/invalid |
| `MissingCredentialGroup` | Device has no credential section configured at all for this sensor type |
| `SensorNeedsProbeDevice` | Sensor can only be created on a probe device (not a regular device) |
| `SensorNeedsLocalProbe` | Requires a local probe connection |
| `ProbeIsDisconnected` | Probe is offline |

**Important:** `MissingCredentialGroup` does not always block creation. Try creating anyway — some sensors succeed despite the hint (e.g. Zoom, SIMATIC S7 sensors created successfully with this hint present).

---

## Sensor Categories by Creation Method

### Direct POST (no metascan)

Sensors with no `HasMetaScan` flag. Build body from POST schema required fields + any known settings.

```python
body = {"basic": {"name": "My Sensor"}}
# Add required fields from POST schema
result = client.request('POST', f'experimental/devices/{device_id}/sensor?kindid={kind}', body)
```

### Metascan-required sensors

Sensors with `HasMetaScan` in their flags. Must run metascan first; POST body includes the metascan selection.

```python
items = client.request('POST', f'experimental/devices/{device_id}/metascan?kind={kind}', {})
# items = [{"disk": "C:", "info": {...}}, ...]

# Get metascan_field path from the schema's additionalProperties
metascan_field = "diskfree.disk"  # from schema
section, key = metascan_field.split('.', 1)  # "diskfree", "disk"

body = {
    "basic": {"name": f"Disk Free {items[0][key]}"},
    section: {key: [item[key] for item in items]}  # all discovered values
}
result = client.request('POST', f'experimental/devices/{device_id}/sensor?kindid={kind}', body)
```

### Sensors that cannot be created via API

| Category | Examples |
|----------|---------|
| Probe-only (`SensorNeedsProbeDevice`) | Some internal sensor types |
| PRTG-autonomous | Core Health, Probe Health, System Health — auto-created |
| Deprecated | Common SaaS, SFTP Secure File Transfer Protocol |
| Require TLS cert/key files | Docker Container Status |
| Exchange/Active Directory | Require domain admin creds via IT ticket |

---

## File Dependencies

Certain sensor kinds require files to be present on the PRTG server or probe **before** the sensor can be created. See `prtg_file_deployments.md` for the full list.

Examples:
- **SNMP Custom String Lookup** — requires a `.ovl` lookup file in `PRTG Network Monitor\lookups\custom\` on the core server, reloaded via Admin Tools
- **SSH Script / SSH Script Advanced** — requires the script file in `PRTG Network Monitor\Custom Sensors\ssh\` on the probe
- **EXE/Script** sensors — require the script in `PRTG Network Monitor\Custom Sensors\EXEXML\`

---

## Practical Error Handling

| HTTP Status | Typical cause | Action |
|------------|---------------|--------|
| `400 BAD_REQUEST` | Missing required field, type mismatch, validation failure | Read `message` field for field name + reason; fix and retry |
| `400 EOF` | Empty metascan body | Add `{}` as body |
| `502 BAD_GATEWAY` | Infrastructure not reachable, or PRTG internal error | Check device connectivity; some are permanent failures |
| `503` / timeout | Metascan timeout regression | Skip sensor; retry after PRTG fix |

Error message parsing tip — extract the cause from verbose errors:

```python
msg = error_data.get('message', '')
if 'Cause:' in msg:
    cause = msg.split('Cause:', 1)[1].strip().split('\n')[0][:200]
```

---

## Setting Lookups for `lookupfilelist` Fields

Some fields (e.g. SSH script file picker) use class `lookupfilelist` with `editOnRequest: true`. These require a metascan to populate valid values. The metascan returns the available options; pass the selected value back in the POST body.

For `lookuplist` fields with a resolvable `lookupkey`:

```python
# Check that the endpoint exists before using it
lookups = client.get(f'setting-lookups/{lookupkey}?id={object_id}')
# Returns items with info.C0 (value to send) and info.C1 (display label)
value_to_send = lookups[0]['info']['C0']
```

`setting-lookups/valuelookups` works correctly (returns 261 results).
`setting-lookups/lookups` returns 404 (broken — see Bug 3).
