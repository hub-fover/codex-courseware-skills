# Codex Courseware Skills

Reusable Codex skills for turning visual-course inputs into verified scripts and then producing numbered Research visual pages.

## Included skills

- `planning-courseware-scripts`: build a course outline, 13-field page scripts, source mapping, and unified review artifacts from knowledge cards, references, and course metadata.
- `producing-research-visual-pages`: run a one-page-at-a-time Research visual workflow with screenshot QA, versioned repairs, and a hard gate before advancing.

The skills are self-contained under `skills/` and follow the Codex `SKILL.md` layout. Supporting references, validators, and UI metadata are included where the skill needs them.

## Install

### PowerShell

```powershell
.\install.ps1
```

### macOS/Linux

```bash
./install.sh
```

The installer copies both skill directories into the current user's Codex skills directory (`~/.codex/skills`). Existing directories are replaced only after the installer asks for confirmation.

## Manual install

Copy `skills/planning-courseware-scripts` and `skills/producing-research-visual-pages` into `~/.codex/skills/`.

## Typical use

1. Use `planning-courseware-scripts` to create and validate the outline, five-page script batches, unified review report, and unresolved-items file.
2. Obtain one unified script confirmation before image generation.
3. Use `producing-research-visual-pages` in a signed-in Research visual browser session. Generate one page, open the actual preview, save the QA screenshot, and lock or repair that page before continuing.

Original images are not downloaded by the visual-production skill unless the user explicitly requests it.

## License

MIT. See `LICENSE`.
