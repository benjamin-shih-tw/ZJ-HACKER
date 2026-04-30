# Phase 1 Driving Tuning

## Three Standard Test Routes

- `straight` (hotkey `7`): emphasizes stability at high speed.
- `curves` (hotkey `8`): emphasizes steering predictability and correction control.
- `hills` (hotkey `9`): emphasizes mixed speed transitions and comfort.

## Feel Scoring Framework

Each test run lasts 60 seconds and outputs:

- `steeringPredict` (0-100)
- `brakingControl` (0-100)
- `speedFeel` (0-100)
- `motionComfort` (0-100)
- `total` = average of the four metrics

## AB Test Rule

- Session initializes `driveAB` to `A` or `B`.
- `A`: baseline acceleration and steering response.
- `B`: slight accel reduction and steering boost.
- Compare KPI by variant:
  - average session length
  - preset switch frequency
  - track test total score

## Standard Test Workflow

1. Keep same route mode and same preset for one full 60s run.
2. Run each route (`7`, `8`, `9`) at least once for each preset.
3. Repeat under both AB variants across multiple sessions.
4. Export data with `F4` and review by preset + AB group.

## Export Schema

CSV columns:

- `ts`
- `ab`
- `preset`
- `mode`
- `total`
- `steeringPredict`
- `brakingControl`
- `speedFeel`
- `motionComfort`

## Preset Recommendation Rule

- New player default: `balanced`.
- If `motionComfort < 65`: suggest `casual`.
- If `speedFeel > 80` and `steeringPredict > 75`: suggest `pro`.
