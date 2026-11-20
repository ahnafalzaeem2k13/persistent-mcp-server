"""Install/verify the pinned Playwright Chromium browser for Colab QA."""
from __future__ import annotations
import importlib.util
import importlib.metadata
import subprocess
import sys

PIN = "playwright==1.65.2"
if importlib.util.find_spec("playwright") is None:
    subprocess.run([sys.executable, "-m", "pip", "install", PIN], check=True)

from playwright.sync_api import sync_playwright

def launch_smoke():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        try:
            page = browser.new_page()
            page.set_content("<title>Colab browser ready</title><h1>ready</h1>")
            assert page.title() == "Colab browser ready"
            print(f"PLAYWRIGHT_READY version={importlib.metadata.version('playwright')} chromium={browser.version}")
        finally:
            browser.close()

try:
    launch_smoke()
except Exception as first_error:
    print(f"Initial Chromium launch failed: {type(first_error).__name__}: {first_error}", file=sys.stderr)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    try:
        launch_smoke()
    except Exception:
        subprocess.run([sys.executable, "-m", "playwright", "install-deps", "chromium"], check=True)
        launch_smoke()
