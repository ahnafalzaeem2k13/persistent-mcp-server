# NIGHTLINE Decisions

- Tablet navigation breakpoint: 820px. The previous 700px threshold left desktop navigation visible and crowded at the requested 768px iPad portrait width. Collapse the navigation at 820px while preserving inline desktop navigation.
- Keep the existing hamburger interaction. Use the existing #menuBtn, aria-expanded, and .nav.open behavior; no new navigation framework is needed.
- Persistence: Google Drive is the source of recovery checkpoints; Colab /content is disposable compute. Checkpoint archives exclude .git, dependency caches, and secret files.
- Browser QA: use the existing pinned Playwright 1.65.2 and its managed Chromium; install/repair only if the smoke test fails.
