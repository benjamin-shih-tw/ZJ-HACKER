# Phase 7 Release Guards

## Stability Guards Added

- Global error overlay:
  - Captures `window.error`.
  - Captures `unhandledrejection`.
  - Displays actionable recovery hint instead of silent failure.

## Persistence Guards Added

- Progress persistence (`road-trip-progress`) now saves:
  - wallet, growth, economy config, tuning values
  - weekly challenge state
  - mission stats
- Auto-save every 5 seconds during runtime.
- Save on unload alongside KPI snapshots.

## Weekly Content Guard

- ISO week seed detection is used to auto-refresh weekly challenges.
- Weekly challenge set resets only when week key changes.

## Recovery Controls

- One-click reset save action in UI.
- Clears progress, KPI history, and driving test history.
