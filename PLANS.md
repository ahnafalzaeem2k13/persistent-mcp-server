# NIGHTLINE QA & Recovery Plan

## Goal
Verify NIGHTLINE in real Chromium at 1440×900 and 768×1024, preserve desktop navigation, fix tablet portrait navigation, save a complete Drive checkpoint, prove cold recovery, and publish a GitHub commit.

## Phases
1. Inspect Drive-backed project, active Colab runtime, browser tooling, and recovery workflow.
2. Capture and inspect baseline desktop/tablet screenshots and diagnostics.
3. Apply the 820px tablet navigation breakpoint; verify the menu opens, follows links, and closes.
4. Save a Drive checkpoint with source, plans, TODOs, worklogs, test script, screenshots, and a SHA-256 manifest.
5. Remove only the disposable local project directory, restore from Drive, verify file hashes and Chromium readiness, then repeat smoke QA.
6. Push a focused GitHub commit; retain Drive recovery if remote publication is blocked.

## Acceptance criteria
- [x] Real Chromium desktop 1440×900 and iPad portrait 768×1024 return HTTP 200.
- [x] No page exceptions, console errors, failed requests, or horizontal overflow.
- [x] Tablet portrait uses a working collapsible menu; desktop retains inline navigation.
- [x] Before/after screenshots saved under results/.
- [x] Drive checkpoint archive and SHA-256 manifest verified (39 files; archive and all member hashes match).
- [x] Cold restore passed: deleted only the local project directory, restored all 39 files from Drive with zero hash mismatches, and relaunched Chromium 159.0.8154.6.
- [x] Browser regression report and screenshots generated after the fix.
- [!] GitHub write is blocked by the connected integration (Git Data API 403); prepared a clean local commit and Drive bundle for authenticated push.
