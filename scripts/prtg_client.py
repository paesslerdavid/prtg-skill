#!/usr/bin/env python3
"""
Shared PRTG API client helpers for scripts and ad-hoc automation.

Usage (quick example):
    from prtg_client import PRTGClient
    client = PRTGClient.from_env()
    devices = client.get("experimental/devices", params={"limit": 3000})
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, Generator, Iterable, Optional
from urllib.parse import urlencode


DEFAULT_TIMEOUT = 30


class PRTGError(RuntimeError):
    """Raised for transport, HTTP, or JSON decode failures."""


def load_credentials(credentials_file: Optional[str] = None, cwd: Optional[Path] = None) -> Dict[str, str]:
    """Load PRTG_HOST and PRTG_API_KEY from a .env-style file."""
    workdir = cwd or Path.cwd()
    candidates: Iterable[Path]
    if credentials_file:
        candidates = [Path(credentials_file)]
    else:
        candidates = sorted(
            p for p in workdir.glob("*.env") if p.name != ".env.example"
        )

    for path in candidates:
        if not path.exists():
            continue
        env: Dict[str, str] = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            raw = line.strip()
            if not raw or raw.startswith("#") or "=" not in raw:
                continue
            key, value = raw.split("=", 1)
            env[key.strip()] = value.strip()
        host = env.get("PRTG_HOST", "").rstrip("/")
        api_key = env.get("PRTG_API_KEY", "")
        if host and api_key:
            return {"host": host, "api_key": api_key, "source": str(path)}

    raise FileNotFoundError(
        "No .env file with PRTG_HOST and PRTG_API_KEY found in working directory."
    )


def encode_filter(filter_expression: str, **extra_params: Any) -> str:
    """Build query string with properly encoded filter syntax."""
    params: Dict[str, Any] = {"filter": filter_expression}
    params.update(extra_params)
    return urlencode(params)


class PRTGClient:
    """Small wrapper around curl to keep scripts deterministic and dependency-light."""

    def __init__(
        self,
        host: str,
        api_key: str,
        timeout: int = DEFAULT_TIMEOUT,
        insecure: bool = True,
    ) -> None:
        self.host = host.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.insecure = insecure

    @classmethod
    def from_env(
        cls, credentials_file: Optional[str] = None, timeout: int = DEFAULT_TIMEOUT
    ) -> "PRTGClient":
        creds = load_credentials(credentials_file=credentials_file)
        return cls(host=creds["host"], api_key=creds["api_key"], timeout=timeout)

    def _build_v2_url(self, path: str, params: Optional[Dict[str, Any]] = None) -> str:
        normalized = path.lstrip("/")
        if normalized.startswith("api/v2/"):
            base = f"{self.host}/{normalized}"
        elif normalized.startswith("v2/"):
            base = f"{self.host}/api/{normalized}"
        else:
            base = f"{self.host}/api/v2/{normalized}"
        if params:
            return f"{base}?{urlencode(params)}"
        return base

    def _build_v1_url(self, path: str, params: Optional[Dict[str, Any]] = None) -> str:
        normalized = path.lstrip("/")
        base = f"{self.host}/api/{normalized}"
        query = dict(params or {})
        query["apitoken"] = self.api_key
        return f"{base}?{urlencode(query)}"

    @staticmethod
    def _redact_url(url: str) -> str:
        if "apitoken=" not in url:
            return url
        token_start = url.find("apitoken=") + len("apitoken=")
        token_end = url.find("&", token_start)
        if token_end == -1:
            token_end = len(url)
        return f"{url[:token_start]}REDACTED{url[token_end:]}"

    def _curl(self, method: str, url: str, body: Optional[Dict[str, Any]] = None) -> str:
        cmd = [
            "curl",
            "-sS",
            "-X",
            method.upper(),
            url,
        ]
        if self.insecure:
            cmd.insert(2, "-k")
        cmd += ["-H", f"Authorization: Bearer {self.api_key}"]
        if body is not None:
            cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(body)]

        run = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=self.timeout,
        )
        if run.returncode != 0:
            raise PRTGError(
                f"curl failed (exit={run.returncode}) for URL {self._redact_url(url)}: {run.stderr.strip()[:300]}"
            )
        return run.stdout

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Call API v2 and decode JSON when content exists."""
        url = self._build_v2_url(path, params=params)
        raw = self._curl(method, url, body=body)
        if not raw.strip():
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            preview = raw.strip()[:300]
            raise PRTGError(f"Failed to decode JSON from {url}: {preview}") from exc

    def get(self, path: str, *, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.request("GET", path, params=params)

    def get_v1(self, path: str, *, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Call API v1 using apitoken query parameter.

        Use only as fallback when v2 lacks required fields.
        """
        url = self._build_v1_url(path, params=params)
        cmd = ["curl", "-sS"]
        if self.insecure:
            cmd.append("-k")
        cmd.append(url)
        run = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=self.timeout,
        )
        if run.returncode != 0:
            raise PRTGError(
                f"curl failed (exit={run.returncode}) for URL {self._redact_url(url)}: {run.stderr.strip()[:300]}"
            )
        if not run.stdout.strip():
            return None
        try:
            return json.loads(run.stdout)
        except json.JSONDecodeError as exc:
            preview = run.stdout.strip()[:300]
            raise PRTGError(
                f"Failed to decode JSON from v1 {self._redact_url(url)}: {preview}"
            ) from exc

    def iter_pages(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        limit: int = 3000,
        max_pages: Optional[int] = None,
    ) -> Generator[list, None, None]:
        """Yield list pages from offset/limit pagination endpoints."""
        offset = 0
        page_count = 0
        base_params = dict(params or {})
        while True:
            page_params = dict(base_params)
            page_params.update({"limit": limit, "offset": offset})
            page = self.get(path, params=page_params)
            if not isinstance(page, list):
                raise PRTGError(
                    f"Expected list page from '{path}', got: {type(page).__name__}"
                )
            yield page
            page_count += 1
            if len(page) < limit:
                break
            if max_pages is not None and page_count >= max_pages:
                break
            offset += limit

    def fetch_all(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        limit: int = 3000,
        max_pages: Optional[int] = None,
    ) -> list:
        data: list = []
        for page in self.iter_pages(path, params=params, limit=limit, max_pages=max_pages):
            data.extend(page)
        return data


def redact(value: str, keep_start: int = 4, keep_end: int = 3) -> str:
    """Safe token redaction for logs."""
    if not value:
        return ""
    if len(value) <= keep_start + keep_end:
        return "*" * len(value)
    return f"{value[:keep_start]}{'*' * (len(value) - keep_start - keep_end)}{value[-keep_end:]}"


if __name__ == "__main__":
    creds = load_credentials()
    print(f"Host: {creds['host']}")
    print(f"Token: {redact(creds['api_key'])}")
    client = PRTGClient(host=creds["host"], api_key=creds["api_key"])
    devices = client.get("experimental/devices", params={"limit": 1})
    print(f"Connectivity check succeeded. Devices sample type: {type(devices).__name__}")
