# FINN — Segment-First Homepage (A/B test prototype)

A clickable prototype for the interview: replace the search-led homepage entry with
three choices, and route each into a flow built for it. **Two variants are built**,
and the badge in the bottom-right switches between them at any time:

- **Variant B — by need:** Klein · Familie · Sport
- **Variant C — by drivetrain:** Elektro · Hybrid · Benzin & Diesel

## Open it

Double-click `index.html`. No server, no build step, no internet needed.
(Optional: `python3 -m http.server 8899` and open http://localhost:8899.)

## Pages

| File | What it is |
|------|------------|
| `index.html` | **Variant B** homepage — hero + three need-based cards. Escape hatch below them. |
| `small.html` | **Value lane.** Price-sorted list, term toggle, budget slider, "what you'd otherwise pay" anchor. No quiz — friction for someone who already knows they want the cheapest. |
| `family.html` | **Guided lane.** Two questions only — how many people, and how they drive. Auto-advance, progress, back button. No budget question: asking it lets the customer anchor low before we have made the safety argument. |
| `family-results.html` | Three cars, not a list: **cheap · safe · premium**, with the middle one visually anchored, badged "Am häufigsten gewählt", and argued on named safety equipment plus a per-day price delta. Deep-linkable: `?size=5&use=trip` (size `2\|4\|5\|7`, use `city\|commute\|trip\|gear`). |
| `sport.html` | **Emotion lane.** Dark, image-led, sorted by desirability. Price appears last and small. |
| `car.html` | Shared PDP. Term + mileage selectors compute real prices. The value argument shown adapts to the segment you arrived from (`?from=small\|family\|sport`). |
| `index-c.html` | **Variant C** homepage — the same hero, cut by drivetrain instead of by need. |
| `drive.html` | Variant C's listing, one page for all three drivetrains (`?type=elektro\|hybrid\|verbrenner`). Each gets its own argument: €/100 km for electric, "no cable needed" for hybrid, choice and simplicity for petrol. |
| `ab-test.html` | The experiment brief: hypothesis, segment psychology, a B-vs-C comparison, metrics, sizing, risks, rollout. |

## What's real

102 vehicles pulled from finn.com — prices, term and mileage packages, equipment
lists, specs and photos. The tier scoring, the three-tier anchoring, the term/mileage
price maths and the €/100 km comparison all compute on that data, not on placeholders.

One finding worth mentioning in the interview: FINN's own `fuel` field labels 21 of
these hybrids as "Benzin" — only the engine string gives them away. Variant C derives
a real `drive_type` from both. A drivetrain-first homepage is only as good as that field.

Open the browser console to watch the tracking events fire: `segment_selected`,
`quiz_answer`, `quiz_completed`, `tier_click`, `km_upsell`, `checkout_start`.

## Structure

```
index.html   small.html family.html family-results.html sport.html   ← variant B
index-c.html drive.html                                             ← variant C
car.html ab-test.html                                               ← shared
assets/
  style.css     one stylesheet, no framework
  app.js        shared header/footer/card/tracking helpers
  data.js       the 102 vehicles (window.CARS)
  cars/         102 vehicle photos
  ui/           hero + lifestyle images
  fonts/        Inter + Suisse Intl (as used by finn.com)
```

Build scripts (`extract.py`, `build_data.py`) and the scraped source pages
(`home.html`, `auto.html`, `pages/`, `cars_raw.json`, `_icons.html`, `.shots/`)
are kept for provenance and are **excluded from the shareable zip**.

---
Built by Gabe Grigorov as a discussion prop. Not a FINN product.
Imagery and vehicle data belong to FINN.
