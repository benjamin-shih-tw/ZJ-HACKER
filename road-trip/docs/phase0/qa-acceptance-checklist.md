# QA Acceptance Checklist

Use this checklist as the release gate for every implementation phase.

## 1) Functional Validation

- [ ] Vehicle movement works on keyboard inputs.
- [ ] Drive preset switching applies expected handling changes.
- [ ] Mission progression updates correctly for micro/mid/weekly tiers.
- [ ] POI interactions grant expected rewards and trigger checks.
- [ ] Challenge progression and completion rewards work without duplicates.

## 2) Data And Progression Validation

- [ ] Economy conversion does not allow negative balances.
- [ ] Upgrade purchases consume correct cost and apply growth correctly.
- [ ] Pity logic triggers only after threshold and resets on success.
- [ ] KPI snapshots persist and load valid JSON from local storage.

## 3) UX Validation

- [ ] HUD information is readable at 1080p and 1440p.
- [ ] Prompt and panel hotkeys (`F2`, `F3`, `1-3`, `7-9`, `J`, `P`) are discoverable.
- [ ] New session starts in a valid default state.
- [ ] No blocking UI overlaps during minigame interactions.

## 4) Performance Validation

- [ ] No major FPS drop during terrain streaming.
- [ ] No memory growth from repeated panel open/close.
- [ ] 20-minute session runs without gameplay-breaking hitches.

## 5) KPI Gates

- [ ] 10-minute retention proxy scenario can be completed without dead ends.
- [ ] Session length test reaches 25 minutes without progression stall.
- [ ] Mission completion rate in test run exceeds 55%.
- [ ] Share event flow can be triggered and recorded multiple times.

## 6) Sign-off

- [ ] Design sign-off
- [ ] Engineering sign-off
- [ ] QA sign-off
- [ ] Ready for next phase
