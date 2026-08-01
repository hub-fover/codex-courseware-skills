---
name: producing-research-visual-pages
description: Use when producing a numbered series of Research visual courseware images from page scripts in a signed-in browser, especially when each page must be visually accepted before the next page and the user will download originals later.
---

# Producing Research Visual Pages

## Principle

Generate one page, inspect it, and lock it before advancing. A failure blocks later pages regardless of deadline or cost.

## Setup

Confirm the master, anchor, scripts, range, exact metadata, filenames, and prohibitions. Uploads may be grouped; generation may not.

## Per-Page Loop

1. Keep the signed-in Research visual conversation; do not switch to Presentation or a new chat.
2. Request one page and state that the previous accepted page is locked.
3. Require one independent 16:9 image using the complete current-page script.
4. Repeat exact fixed text, title, page number, formulas, steps, prohibitions, and filename.
5. Require readable type and clear whitespace; forbid extra copy that shrinks text.
6. Wait, open the preview, and save a QA screenshot. Do not download originals unless explicitly requested.
7. Pass the rendered image through the gate below.
8. Pass: lock candidate/version and advance one page. Fail: request `v02`, `v03`, etc. with exact defects; do not advance.

## Acceptance Gate

All must pass:

- exact title, chapter strip, footer, and `current/total`
- all required formulas, symbols, steps, and conclusions
- no prohibited content, copied text, montage, duplicate, or watermark
- no typo, truncation, overlap, clipping, or incoherent layout
- readable text, formulas, labels, and legends
- visible outer/inter-module whitespace; no small-text packing
- correct candidate when multiple images appear

Response text and image descriptions are not evidence. Judge the rendered screenshot.

## Repair

Name the failed version and defects, preserve locked content, and request only that page. For density, remove only non-script copy, enlarge text/formulas, simplify modules, and add spacing. Never alter required fields.

Example:

```text
Page 31 is accepted and locked. Generate page 32 only from its complete script.
Require exact fixed text, formulas, 32/40, readable type, and clear whitespace.
Return one independent 16:9 Research visual image; modify no other page.
```

## Batch And Handoff

- Batch upload/reporting are allowed; batch generation/acceptance are not.
- Review screenshots together only after each page already passed individually.
- Save stable names such as `course-pNN-check.png`.
- After the final pass, verify screenshots, leave the conversation open, and let the user download originals.

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "The site supports ten images" | Capacity does not replace per-page acceptance. |
| "Fix the defect later" | An unresolved page blocks all later pages. |
| "Small text is still present" | Uncomfortable reading is failure. |
| "The description says it is correct" | Only the rendered screenshot is evidence. |
| "Download now for safety" | Preserve screenshots and the live conversation unless the user changes that decision. |

Any such thought means stop and return to the current page gate.

See [evaluations.md](evaluations.md) when testing or revising this skill.
