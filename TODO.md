# NIGHTLINE TODO

- [x] Locate NIGHTLINE project, active Colab runtime, mounted Drive, and recovery notebook.
- [x] Reproduce the tablet portrait header crowding at 768×1024 from the retained baseline screenshot.
- [x] Apply the 820px breakpoint so desktop links collapse to the existing accessible menu on tablet.
- [x] Run Playwright Chromium at desktop 1440×900 and tablet 768×1024; both HTTP 200, no overflow, page errors, console errors, or failed requests.
- [x] Verify tablet menu opens (aria-expanded=false → true), follows the Network link, and closes; desktop nav remains inline.
- [x] Verify route selection and pause/resume motion controls.
- [x] Capture matching before/after desktop and tablet viewport screenshots plus full-page captures.
- [x] Save full Drive checkpoint and verify archive/manifest SHA-256 and all 39 member hashes.
- [x] Delete only local /content/persistent-mcp-server, restore from Drive, and verify all file hashes plus Playwright/Chromium launch.
- [!] Push requires interactive GitHub authentication: GitHub API returned 403 Resource not accessible by integration; Colab git push has no configured username. Prepared commit and Drive bundle are ready.
