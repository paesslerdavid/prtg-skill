# Error Handling Guide

Use this reference when PRTG API calls fail or return partial data.

## HTTP Status Triage

## 400 Bad Request

- Usually invalid query/filter/body shape.
- Re-check filter quoting rules and enum casing.
- Validate section names for patch payloads.

## 401 Unauthorized

- Token missing/invalid/expired.
- Verify `Authorization: Bearer <token>` for v2.
- Verify `.env` file selection when multiple `.env` files exist.

## 403 Forbidden

- Token is valid but lacks rights for the target object/action.
- Confirm object permissions and account role.

## 404 Not Found

- Wrong endpoint path or object ID.
- Check singular/plural endpoint path differences.
- For visualization modules, allow targeted v1 fallback when v2 path is missing.

## 409 Conflict

- Concurrent state change or invalid transition.
- Re-read object, rebuild patch from latest state, retry once.

## 429 Too Many Requests

- Apply exponential backoff with jitter.
- Reduce parallel request fan-out.
- Process writes in smaller batches.

## 5xx Server Errors

- Treat as transient unless repeated.
- Retry with capped backoff (for example 1s, 2s, 4s).
- If persistent, switch to read-only diagnostics and report failure context.

## Response Shape Guardrails

- List endpoints return arrays, not `{ "items": [...] }`.
- IDs are strings for filters and `in` expressions.
- Timeseries headers are channel IDs and require channel name mapping.

## Retry Strategy

Retry:
- `429`
- `500`, `502`, `503`, `504`

Do not retry without modification:
- `400`, `401`, `403`, `404`, `409`

## Logging Rules

- Never print raw API keys.
- Log endpoint, method, status, and short error snippet.
- Include object IDs in failures for resumable batch execution.

## Fallback Policy

1. Try v2 endpoint first.
2. If response indicates unsupported/missing capability (`404/501` or missing required fields), use v1 only for that module.
3. Disclose v1 usage explicitly in output.
