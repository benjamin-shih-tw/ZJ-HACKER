# Phase 2 Event Trigger Table

## Mission Trigger Sources

- `poi_interact`: increments interaction-based missions.
- `pulse_reward`: increments pulse-based missions.
- `quest_done`: increments weekly mission throughput.
- `photo_share`: increments share-based missions.
- `distanceKm`: feeds drive-distance missions.

## Trigger -> Mission Mapping

- Fishing success
  - `m_fish2`
  - `d_fish8`
- Chopping/mining outputs
  - `m_wood3`
  - `m_stone3`
  - `d_wood10`
- Camp cooking
  - `m_food2`
- POI interactions
  - `m_poi3`
  - `d_poi6`
- Drive distance
  - `m_drive1k`
  - `w_drive12k`
- Share marker
  - `d_shares3`
  - `w_share4`
- Reward pulse
  - `d_pulses3`
  - `w_pulse10`
