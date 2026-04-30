# Phase 2 Mission Rework

## Three-Layer Mission Model

- `micro` (2-5 minutes): fast completion and frequent reward.
- `mid` (10-20 minutes): capability checks and progression pushes.
- `weekly` (long horizon): retention anchor and meta upgrades.

## Active Mission Slots

- 2 micro + 2 mid + 1 weekly active concurrently.

## Weighted Pool Mechanism

- Missions have `weight`.
- Picker excludes `done` and currently `active` entries.
- On completion, only same-tier replacement is rolled.

## POI Binding Strategy

- Fishing/chopping/mining/camping outcomes directly contribute to mission checks.
- Every mission completion updates session metrics and reward economy.

## Output Targets

- At least 12 templates available in total.
- Completion cadence target:
  - micro every 3-6 minutes
  - mid every 12-20 minutes
  - weekly at least once per long session window
