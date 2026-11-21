# Worklog

2026-11-21: Expanded Zaeem Tools from 24 to 50 tools in 11 categories. Added compound interest, loan EMI, average/statistics, random picker, fractions, area, number-base and Roman numeral conversion, lorem ipsum, find/replace, whitespace cleaning, word frequency, text diff, binary, UUID, JWT decode, regex testing, Unix timestamps, HTML entities, CSV↔JSON, local image resize/compression, QR generation, color palettes, Pomodoro focus/break cycles, and GPA. Added copy-result buttons, accessible labels, responsive focus styling, PWA manifest/icon/service worker.

QA evidence: Node syntax check passed. Playwright opened and closed all 50 tools with zero page errors. Representative outputs verified: loan EMI 2075.84/month for 100000 at 9% over 5 years; binary 1010→decimal 10; CSV→JSON two records; GPA 3.43; 1/2 + 1/3 = 5/6. Image resize generated a downloadable PNG fixture output. Currency v2 returned USD→BDT 124.6400 (rate date 2026-11-20). Offline reload restored all 50 cards. No horizontal overflow at 1440×900, 1024×1366, or 390×844.

External dependencies: Google Fonts, Frankfurter reference-rate API, and QR Server QR-image API. QR content is sent to the external QR service; do not enter private content. Currency reference rates are not trading quotes.


2026-11-21: User clarified preference for practical tools, not colour and theme features. Removed colour picker, contrast checker, palette generator, Color category and theme toggle. Replaced the category with four real PDF workflows: merge PDFs, extract page ranges, rotate pages, and convert multiple JPG/PNG images into an A4/Letter/custom-fit PDF. PDF operations run locally with pdf-lib.

2026-11-21: Clarified that the request was a full website redesign, not removal of the theme tools. Preserved the full 53-tool catalogue including colour utilities; restored Color category and website light/dark appearance toggle. Rebuilt the UI styling with a premium midnight-navy and periwinkle visual system, improved cards, navigation, search, forms, responsive layout, focus states and motion preferences.
