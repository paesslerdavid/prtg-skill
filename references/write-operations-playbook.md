# Write Operations Playbook

Use this guide for any task that changes PRTG state (`POST`, `PATCH`, `DELETE`).

## Safety Defaults

1. Start in read mode and gather object IDs plus current values.
2. Build a dry-run plan that shows:
   - endpoint + method
   - object IDs and names
   - field-level before/after values
   - blast radius (how many objects affected)
3. Ask for explicit confirmation before executing write calls.
4. Execute writes in small batches (5-20 objects).
5. Re-read affected objects and confirm expected state.

## Dry-Run Plan Format

Use this structure before writes:

```text
Plan:
- PATCH /experimental/sensor/2490
  - basic.name: "Old Name" -> "New Name"
- PATCH /devices/42
  - discoverytypegroup.discoverytype: "0" -> "1"
Impact: 2 objects, no deletes
Rollback: restore previous values with PATCH using captured "before" fields
```

## High-Risk Operations

- `DELETE` operations (sensor/device/group removal)
- Bulk pause/resume or bulk acknowledge
- Group/device setting changes affecting child object behavior
- Auto-discovery and scan interval changes

For high-risk operations, capture pre-change snapshots to local JSON before execution.

## Rollback Patterns

## Rename / setting change rollback

1. Read current object.
2. Save full section being modified.
3. Apply PATCH.
4. On failure or regression, PATCH saved section back.

## Delete rollback

Deletion is not reversible by API. Before delete:

1. Export object settings + parent ID.
2. Record sensor type (`kindid`) and name.
3. Recreate under original parent if needed, then restore key settings.

## Acknowledge / pause rollback

- Acknowledge rollback: clear acknowledgment where endpoint supports reset flow.
- Pause rollback: `POST /devices/{id}/resume` or relevant resume endpoint.

## Batch Write Guardrails

- Stop batch on first non-2xx response.
- Retry only `429` and transient `5xx` with backoff.
- Never retry `4xx` blindly.
- Emit a final table with per-object result (`success`, `failed`, `rolled back`).

## Endpoint Notes

- Sensor patch bug: use `PATCH /experimental/sensor/{id}` (singular).
- Use `include=all_sections` when reading settings before patching.
- Use API v2 first; use v1 only when required fields are unavailable.
