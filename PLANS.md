# NIGHTLINE QA & Recovery Plan

## Goal
Verify NIGHTLINE desktop and iPad layouts, fix tablet navigation, preserve evidence in Drive, prove cold recovery, and publish to GitHub.

## Completed phases
1. Inspected project, Drive checkpoint workflow, Colab runtime, and browser tooling.
2. Captured baseline desktop/tablet screenshots and diagnostics.
3. Fixed tablet header at the 820px breakpoint; verified hamburger open, navigation, and close behavior.
4. Saved Drive checkpoints and SHA-256 manifests.
5. Deleted the disposable local workspace, restored from Drive, verified hashes, and reran browser smoke/QA.
6. Published commit `2b8e82373af3aa29a2279ed380aecca6ad70e66f` to GitHub `main`; remote hash matched local HEAD.

## Acceptance
- [x] Real Chromium at desktop 1440×900 and tablet 768×1024.
- [x] No page exceptions, console errors, failed requests, or horizontal overflow.
- [x] Tablet menu opens, navigates, and closes; desktop inline nav remains intact.
- [x] Before/after viewport and full-page screenshots saved in `results/`.
- [x] Drive checkpoint archive and SHA-256 manifest verified.
- [x] Cold restore from Drive and browser readiness verified.
- [x] GitHub push confirmed; remote `main` equals local commit.
