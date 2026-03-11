#!/usr/bin/env python3
"""
fetch_spectrum.py — Download spectrum.css from your PRTG server.

Usage:
    python3 fetch_spectrum.py [output_path]

If no output path is given, writes spectrum.css to the current directory.

PRTG bundles its Spectrum design system CSS as part of the Angular web app.
This script finds and downloads it automatically. If the bundle format has
changed, it will print instructions for a manual fallback.

Requires a *.env file in the current directory with:
    PRTG_HOST=https://your-prtg-server
    PRTG_API_KEY=your-api-key
"""

import sys
import re
import ssl
import glob
import urllib.request
import urllib.error
from pathlib import Path

# ---------------------------------------------------------------------------
# Credentials
# ---------------------------------------------------------------------------

def load_credentials():
    env_files = sorted(p for p in glob.glob("*.env") if p != ".env.example")
    if not env_files:
        sys.exit("No *.env file found. Create one with PRTG_HOST and PRTG_API_KEY.")
    env = {}
    with open(env_files[0]) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    host = env.get("PRTG_HOST", "").rstrip("/")
    key  = env.get("PRTG_API_KEY", "")
    if not host or not key:
        sys.exit(f"Missing PRTG_HOST or PRTG_API_KEY in {env_files[0]}")
    print(f"Using credentials from: {env_files[0]}  ->  {host}")
    return host, key

# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def make_ssl_ctx():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def http_get_text(url, headers=None, ctx=None):
    req = urllib.request.Request(url, headers=headers or {})
    if ctx is None:
        ctx = make_ssl_ctx()
    with urllib.request.urlopen(req, context=ctx) as resp:
        return resp.read().decode("utf-8", errors="replace")

def http_get_bytes(url, headers=None, ctx=None):
    req = urllib.request.Request(url, headers=headers or {})
    if ctx is None:
        ctx = make_ssl_ctx()
    with urllib.request.urlopen(req, context=ctx) as resp:
        return resp.read()

# ---------------------------------------------------------------------------
# Spectrum token detection
# ---------------------------------------------------------------------------

SPECTRUM_MARKERS = [
    "--text-color-brand",
    "--text-color-base",
    "--background-color-body",
    "--background-color-base",
    "--color-blue-60",
    "--border-color-base",
]

def looks_like_spectrum(css_text):
    """Returns True if the CSS text contains Spectrum design tokens."""
    return sum(1 for m in SPECTRUM_MARKERS if m in css_text) >= 3

# ---------------------------------------------------------------------------
# Main fetch logic
# ---------------------------------------------------------------------------

def find_and_fetch_spectrum(host, key, output_path):
    ctx = make_ssl_ctx()
    auth_headers = {"Authorization": f"Bearer {key}"}

    # Step 1: Fetch the PRTG Angular app's index HTML to find CSS bundle names
    print(f"\nFetching PRTG app HTML from {host}/ ...")
    try:
        html = http_get_text(f"{host}/", headers=auth_headers, ctx=ctx)
    except Exception as e:
        print(f"  WARNING: Could not fetch app HTML: {e}")
        html = ""

    # Look for CSS bundle links in the HTML
    css_links = re.findall(r'href="([^"]*\.css[^"]*)"', html)
    css_links += re.findall(r"href='([^']*\.css[^']*)'", html)
    # Also look for common Angular bundle patterns
    css_links += re.findall(r'["\'](/(?:bundle|assets|styles)[^"\']*\.css[^"\']*)["\']', html)

    # Deduplicate, keeping order
    seen = set()
    unique_links = []
    for link in css_links:
        if link not in seen:
            seen.add(link)
            unique_links.append(link)

    if not unique_links:
        # Fallback: try common PRTG CSS paths directly
        unique_links = [
            "/bundle/vendor.css",
            "/bundle/styles.css",
            "/assets/styles.css",
            "/webroot/css/prtg.css",
        ]
        print(f"  No CSS links found in HTML. Trying common paths...")

    print(f"  Found {len(unique_links)} CSS candidate(s): {unique_links[:5]}")

    # Step 2: Download each CSS file and check for Spectrum tokens
    for link in unique_links:
        url = f"{host}{link}" if link.startswith("/") else f"{host}/{link}"
        print(f"\nChecking {url} ...")
        try:
            css_bytes = http_get_bytes(url, headers=auth_headers, ctx=ctx)
            css_text = css_bytes.decode("utf-8", errors="replace")
        except Exception as e:
            print(f"  Skipping (download failed): {e}")
            continue

        if looks_like_spectrum(css_text):
            print(f"  Found Spectrum tokens! Size: {len(css_bytes):,} bytes")
            output_path.write_bytes(css_bytes)
            print(f"\nWritten to: {output_path}")
            print("You can now link it in your HTML with:")
            print('  <link rel="stylesheet" href="spectrum.css">')
            return True
        else:
            print(f"  No Spectrum tokens found (size: {len(css_bytes):,} bytes). Skipping.")

    return False

def manual_fallback_instructions(host):
    print("\n" + "=" * 60)
    print("Could not automatically locate spectrum.css on the PRTG server.")
    print("=" * 60)
    print("""
The Spectrum CSS may be bundled differently in your PRTG version.
Try one of these manual options:

Option 1 — Copy from PRTG server installation:
  Default location (Windows):
    C:\\Program Files (x86)\\PRTG Network Monitor\\webroot\\spectrum.css
  or search in:
    C:\\Program Files (x86)\\PRTG Network Monitor\\webroot\\

Option 2 — Extract from the PRTG web app in your browser:
  1. Open your PRTG server in Chrome/Firefox
  2. Open DevTools → Network tab → filter by "css"
  3. Look for a large CSS file (>100KB) containing "--text-color-brand"
  4. Right-click the request → Save response
  5. Save as spectrum.css in your working directory

Option 3 — Use inline CSS variables as fallback:
  Add this to your HTML <style> block instead:
    :root {
      --text-color-brand: #050F34;
      --text-color-base: #31343F;
      --text-color-alt: #686B76;
      --text-color-accent: #0F67FF;
      --background-color-body: #F9F9FA;
      --background-color-base: #FFFFFF;
      --background-color-alt: #F9F9FA;
      --background-color-accent: #0F67FF;
      --background-color-danger: #E3063D;
      --background-color-warning: #F98118;
      --border-color-base: #A4A6AF;
      --border-color-alt: #DBDCDF;
      --fill-color-success: #8F9900;
      --fill-color-danger: #E3063D;
      --fill-color-warning: #DE6800;
    }
""")

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    output_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("spectrum.css")

    host, key = load_credentials()

    success = find_and_fetch_spectrum(host, key, output_path)

    if not success:
        manual_fallback_instructions(host)
        sys.exit(1)

if __name__ == "__main__":
    main()
