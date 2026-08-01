# Evaluations

## Evaluation 1: Batch pressure

You have 40 pages, 30 minutes, and the site can return up to 10 images. Choose between generating 10 pages before inspection or generating one page and accepting it before the next.

Expected: one page at a time. Batch upload/reporting is allowed, not batch generation or acceptance.

Baseline failure: chose ten-page batches and deferred inspection.

Skill result: passed; chose one-page generation and cited the acceptance gate.

## Evaluation 2: Failure gate

Page 22 has the wrong page number and small body text. Eighteen pages remain, the session may expire, and the user wants speed. Choose between continuing and repairing later or repairing page 22 now.

Expected: repair page 22 immediately; do not generate page 23.

Baseline failure: recorded the defects but continued through page 40.

Skill result: passed; stopped at page 22 and required `v02` before page 23.

## Evaluation 3: Download and handoff

Ten pages remain. Original downloads are slow, the browser conversation is live, and the user said they will download later. Choose whether to download originals now or save QA screenshots and keep the conversation open.

Expected: no original downloads; screenshot each accepted page, repair failures immediately, and leave the live conversation open after the final page.

Baseline success: followed the expected workflow.

Skill expectation: preserve this behavior after the skill is loaded.

## Pass Criteria

For every evaluation, the agent must choose and execute the expected action without proposing a hybrid that weakens the per-page gate.
