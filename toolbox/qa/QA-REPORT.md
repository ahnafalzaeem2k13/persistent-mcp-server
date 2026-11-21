# Zaeem Tools — QA report

Date: 2026-11-21

## Automated checks
- `node --check app.js`: passed.
- Playwright Chromium: 50/50 tool cards opened and returned to the catalogue; zero page errors in the full open/close run.
- Calculations verified: loan EMI (100,000 at 9% for 5 years = 2,075.84/month), fraction (1/2 + 1/3 = 5/6), average (1,2,3,4 = mean/median 2.5, range 3), Roman numeral 2026 = MMXXVI, GPA sample = 3.43.
- Conversion verified: binary 1010 to decimal 10; CSV with quoted-capable parser converted to two JSON records.
- Image resize/compress: generated a downloadable output from a tiny PNG fixture.
- Currency v2: USD→BDT returned 124.6400, rate date 2026-11-20. Reference data only.
- Service worker: registered; offline reload restored the app and all 50 tool cards.
- Responsive viewports: 1440×900, 1024×1366, 390×844; no horizontal overflow.

## Screenshots
- `zaeem-tools-1440x900.png`
- `zaeem-tools-1024x1366.png`
- `zaeem-tools-390x844.png`

## Limitations
- QR images are requested from QR Server; QR input is sent to that external service.
- Currency rates require internet and are indicative reference rates, not real-time trading quotes.
- External font files require internet; system fallback fonts are available.
- Screenshot files were captured by Chromium; they were not independently reviewed pixel-by-pixel by a separate vision model.
