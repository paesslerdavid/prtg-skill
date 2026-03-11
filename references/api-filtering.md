# PRTG API v2 — Filtering & Query Reference

Consolidated reference for PRTG API v2 filter expressions, query parameters, and sorting. Current as of live server spec.

## Common Query Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `offset` | Zero-based index to start from | 0 |
| `limit` | Max results to return (0 = up to 3000) | 100 |
| `filter` | Filter expression (see below) | |
| `sort_by` | Comma-separated fields; prefix `-` for descending, `+` for ascending | |
| `include` | Comma-separated extra data sections to embed in the response. Common values: `sensor_status_summary` (device sensor counts), `all_sections` (all settings sections), `*` (all extras). Example: `?include=sensor_status_summary` | |

**Important:** Set `limit` high (e.g. 3000) when you need all results. The default is only 100.

**Note on `include=sensor_status_summary`:** This is a value of the `include` parameter — **not** a standalone query parameter. Use `?include=sensor_status_summary` to get sensor status counts on device responses. Using `?sensor_status_summary=true` does nothing.

## Filter Syntax

Filters use a **custom expression language** — NOT OData or standard query syntax.

```
filter=<expression>
```

URL-encode the filter value. With curl, use `--data-urlencode 'filter=...' -G` for safe encoding.

### Simple Expressions

```
property operator value
```

### Data Types & Notation

| Type | Notation | Example |
|------|----------|---------|
| Text | `"quoted string"` | `name = "Local Probe"` |
| Number | bare integer | `priority = 1` |
| Boolean | `true` / `false` | `favorite = true` |
| Enumeration | bare identifier | `status = up` |
| List | `[val1, val2]` | `name in ["Core Health", "Probe Health"]` |

### Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equal | `status = up` |
| `!=` | Not equal | `kind != "Probe Device"` |
| `<` | Less than | |
| `<=` | Less or equal | |
| `>` | Greater than | |
| `>=` | Greater or equal | |
| `in` | Value in list | `name in ["Ping v2", "HTTP v2"]` |
| `contains` | Value exists in object values | `basic.tags contains "ping"` |
| `matches` | Fuzzy/similar text match | `name matches "ping"` |

**Warning:** `matches` can be unreliable and return incomplete results. Prefer `=`, `in`, or `contains`.

## Filterable Properties

| Property | Type | Operators | Example |
|----------|------|-----------|---------|
| `id` | Text | `=, !=` | `id = "50"` |
| `name` | Text list | `=, !=, in` | `name in ["Core Health"]` |
| `status` | Enum | `=, !=` | `status = down` |
| `type` | Enum | `=, !=` | `type = sensor` |
| `kind` | Text | `=, !=` | `kind != "Probe Device"` |
| `parentid` | Text | `=, !=, in` | `parentid = "2004"`, `parentid in ["2004","2005"]` |
| `favorite` | Boolean | `=, !=` | `favorite = true` |
| `primary` | Boolean | `=, !=` | `primary = true` (channels) |
| `basic.host` | Text | `=, !=, in` | `basic.host = "192.0.0.1"` |
| `basic.hostv6` | Text | `=, !=, in` | `basic.hostv6 = "::1"` |
| `basic.tags` | Text | `contains` | `basic.tags contains "ping"` |
| `basic.parenttags` | Text | `contains` | `basic.parenttags contains "snmp"` |

**Critical:** `sensor_kind` is NOT a filterable property. To filter sensors by type, use:
- `basic.tags contains "ping"` (tags often match sensor kind)
- `name = "Ping v2"` (if sensor names are predictable)
- Client-side filtering: fetch all sensors and filter by `sensor_kind` in code

## Status Enum Values

For filter expressions, use **lowercase**:

`none`, `unknown`, `collecting`, `up`, `warning`, `down`, `disconnected`, `pausedbyuser`, `pausedbydependency`, `pausedbyschedule`, `unusual`, `pausedbylicense`, `pausedbyuseruntil`, `acknowledged`, `partialdown`

**Critical — filter vs response mismatch:** Device status values **in API responses** are prefixed with `SUMMED_INFO_` (e.g. `SUMMED_INFO_UP`, `SUMMED_INFO_DOWN`), while sensor statuses are plain uppercase (e.g. `UP`, `DOWN`). **Filter expressions always use lowercase without prefix** for both: `filter=status = down`, NOT `filter=status = SUMMED_INFO_DOWN`. Using the response-format values in filters will return `INVALID_FILTER`.

## Type Enum Values

`channel`, `device`, `group`, `library`, `probe`, `sensor`, `user`, `usergroup`

## Complex Expressions

Combine with `and`, `or`, `not()`:

```
type = sensor and status = down
type = sensor and (basic.tags contains "ping" or status = down)
not(basic.tags contains "snmp")
```

Precedence: `not` > `and` > `or`. Use parentheses to override.

## Filtering by Tree Structure

Use `parentid` to scope queries to a subtree:

```
parentid = "2004"
```

**Important:** `parentid` only matches **direct children**, not descendants. For example, sensors belong to devices, not groups. To find all sensors in a group:
1. First query devices with `parentid = "<group_id>"`
2. Then query sensors with `parentid in ["<device_id1>", "<device_id2>", ...]`

## Sorting

Use `sort_by` parameter with field names. Prefix `-` for descending:

```
sort_by=status          # ascending
sort_by=-status         # descending
sort_by=name,-priority  # multi-field
```

## Common Pitfalls

1. **Filter syntax is NOT OData.** Use `=`, `!=`, `contains`, `matches` — not `eq`, `ne`, etc.
2. **Text values must be double-quoted** in filter expressions: `name = "Ping v2"`, not `name = Ping v2`.
3. **Enum values are bare identifiers:** `status = up`, not `status = "up"`.
4. **IDs are always strings** in filters: `parentid in ["2490","2491"]`. Using bare integers like `parentid in [2490]` returns 0 results silently.
5. **`parentid = value` requires a text value** — `parentid = 2490` fails with "value must be a text". Use `parentid = "2490"`.
6. **`parent.id` is NOT filterable** on channels — use `parentid` (flat field). The API returns `INVALID_FILTER` for `parent.id`.
7. **`matches` operator is unreliable** — may return incomplete results. Prefer exact match or `contains`.
8. **Default limit is 100.** Always set `limit=3000` to avoid truncated results.
9. **3000 is not a hard cap for large installations.** If you receive exactly `limit` results, there may be more. Use `offset` + `limit` pagination to retrieve all results: fetch pages until a page returns fewer items than `limit`.
