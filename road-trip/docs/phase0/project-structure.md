# Project Structure Baseline

## Current Structure

```text
road-trip/
  index.html
  assets/
  docs/
    core-loop.md
    visual-bible.md
    liveops-calendar.md
    design/
      phase1-driving-tuning.md
      phase2-mission-rework.md
      phase3-economy-growth.md
      phase4-challenge-loop.md
      phase5-kpi-polish.md
    phase0/
      README.md
      version-scope.md
      project-structure.md
      qa-acceptance-checklist.md
```

## Conventions

- Core runtime remains in `index.html` until module split phase starts.
- Static resources go in `assets/`.
- Design and planning artifacts go in `docs/`.
- Phase-based execution docs go in `docs/design/` and `docs/phase0/`.

## Next Refactor Boundary (Post-Phase 1)

When module split starts, migrate to:

- `src/game/` for runtime logic (vehicle, world, missions, economy).
- `src/ui/` for HUD and panels.
- `src/data/` for mission/challenge/economy tables.
- `tests/` for simulation and regression checks.
