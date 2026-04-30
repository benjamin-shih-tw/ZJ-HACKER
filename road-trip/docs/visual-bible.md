# Stylized Lowpoly Visual Bible

## Design Pillars

- Calm readability first, detail second.
- Landmark silhouettes must be recognizable at distance.
- Warm foreground plus cool sky contrast for screenshot value.

## Palette Tokens

- Base fog sky: `#9dcfef` to `#1a6bbf`
- Road asphalt: `#2e2e2e`
- Ground bands: lowland `#388f33`, midland `#6e9140`, highland `#948f80`
- UI neutral: `#F4F2ED`, `#343c3e`
- Accent warn: `#ff992b`

## Lighting Rules

- Use one strong directional key light and ambient fill.
- Keep soft shadows enabled for depth cues.
- Target golden-hour look via ACES tone mapping exposure near `1.1-1.2`.

## Materials

- Terrain: matte Lambert with vertex colors.
- Vehicle: warm off-white body and muted cabin shades.
- Markers: limited emissive-like bright colors to avoid visual noise.

## Landmark Language

- Forest: clustered conifer stacks and chop marker.
- Lake: circular water body with tree rim and fish marker.
- Camp: tent silhouette and ringed rocks.
- Rocky: dense stones and mining marker.

## UI Visual Rules

- Minimal HUD with translucent glass blocks.
- Monospace for speed metrics, sans for labels.
- Keep interaction prompts centered and concise.
