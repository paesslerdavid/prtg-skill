# Paessler Spectrum Design System — Token Reference

Use `spectrum.css` (extracted from `@paessler/spectrum@28.5.0`) for full CSS with custom properties.
For static HTML dashboards, link `spectrum.css` and use `var(--token-name)` throughout.

## CSS Usage in Static HTML

```html
<link rel="stylesheet" href="spectrum.css">
```

All tokens below are available as CSS custom properties with the naming pattern `--token-name`.
For example, `text-color-brand` becomes `var(--text-color-brand)`.

## Typography

| Token | Value |
|-------|-------|
| **Font family** | |
| `font-family-heading` | Roboto, "Segoe UI", Tahoma, Arial, Helvetica, Verdana, sans-serif |
| `font-family-text` | Roboto, "Segoe UI", Tahoma, Arial, Helvetica, Verdana, sans-serif |
| `font-family-code` | inconsolata, monospace |
| **Font size** | |
| `font-size-x-small` | 10px (0.625rem) |
| `font-size-small` | 12px (0.75rem) |
| `font-size-base` | 14px (0.875rem) |
| `font-size-large` | 16px (1rem) |
| `font-size-h4` | 18px (1.125rem) |
| `font-size-h3` | 20px (1.25rem) |
| `font-size-h2` | 22px (1.375rem) |
| `font-size-h1` | 26px (1.625rem) |
| **Line height** | |
| `line-height-x-small` | 12px |
| `line-height-small` | 16px |
| `line-height-base` | 20px |
| `line-height-large` | 20px |
| `line-height-h4` | 24px |
| `line-height-h3` | 28px |
| `line-height-h2` | 32px |
| `line-height-h1` | 32px |
| **Font weight** | |
| `font-weight-regular` | 400 |
| `font-weight-medium` | 500 |
| `font-weight-bold` | 700 |
| **Letter spacing** | |
| `letter-spacing-base` | 0 |
| `letter-spacing-button` | 0.02em |

## Spacing

Base spacer unit: **4px** (0.25rem). All spacing is multiples of this.

Use multiples: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64px etc.

## Borders

| Token | Value |
|-------|-------|
| `border-size-base` | 1px |
| `border-size-large` | 2px |
| `border-radius-small` | 2px (0.125rem) |
| `border-radius-base` | 4px (0.25rem) |
| `border-radius-large` | 8px (0.5rem) |
| `border-radius-rounded` | 2em |
| `border-radius-circle` | 50% |

## Shadows (Elevation)

| Token | Description |
|-------|-------------|
| `box-shadow-elevation-0` | none |
| `box-shadow-elevation-1` | Subtle — cards, list items |
| `box-shadow-elevation-2` | Medium — dropdowns, popovers |
| `box-shadow-elevation-3` | Prominent — floating panels |
| `box-shadow-elevation-4` | Maximum — modals, dialogs |
| `box-shadow-elevation-inset-1` | Inset shadow for inputs |
| `box-shadow-focus` | Blue focus ring (4px blue-30) |
| `box-shadow-focus-error` | Red focus ring |
| `box-shadow-focus-success` | Green focus ring |

## Opacity

| Token | Value |
|-------|-------|
| `opacity-soft` | 0.75 |
| `opacity-disabled` | 0.5 |

## Z-Index

| Token | Value |
|-------|-------|
| `z-index-popper` | 9999 |
| `z-index-modal` | 8888 |
| `z-index-toast-bar` | 8500 |
| `z-index-menu-drawer` | 7000 |

## Colors — Base Palette

Each color has shades: 0 (lightest), 5, 20, 30, 40, 50, 60, 70, 80, 95, 100 (darkest).

| Color | 50 (primary) | 0 (lightest) | 100 (darkest) |
|-------|-------------|--------------|----------------|
| **Blue** | #2678FF | #F5F9FF | #031B45 |
| **Green** | #B4BF17 | #FDFFEB | #24260B |
| **Red** | #F2174D | #FFF6F8 | #330813 |
| **Salmon** | #F37176 | #FFF7F7 | #381819 |
| **Dark Orange** | #F07000 | #FFF8F3 | #331903 |
| **Yellow** | #F2BE25 | #FFFCF3 | #3B2D04 |
| **Cyan** | #00AEEF | #F6FCFF | #052E3D |
| **Turquoise** | #76D8D6 | #F0FFFF | #213B3A |
| **Magenta** | #DF399D | #FFF7FC | #3D0B29 |
| **Purple** | #814EED | #FAF7FF | #23114A |
| **Beige** | #D7B185 | #FFFCF9 | #382918 |
| **Mint** | #3CE794 | #F4FFFA | #0C3D25 |
| **Grey** | #8B8E98 | #F9F9FA | #1D202B |
| **Black Blue** | #050F34 | — | — |
| **White** | #FFFFFF | — | — |

## Colors — Light Theme (Semantic Tokens)

### Text Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `text-color-brand` | #050F34 | Headings, button text |
| `text-color-base` | #31343F | Normal body text |
| `text-color-alt` | #686B76 | Help text, secondary info |
| `text-color-disabled` | #A4A6AF | Placeholder, disabled text |
| `text-color-accent` | #0F67FF | Links, active state |
| `text-color-accent-alt` | #065AEC | Link hover state |
| `text-color-danger` | #E3063D | Error text |
| `text-color-warning` | #A04B00 | Warning text |
| `text-color-success` | #697000 | Success text |
| `text-color-overlay` | #FFFFFF | Text on dark backgrounds |

### Background Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `background-color-body` | #F9F9FA | Page body |
| `background-color-base` | #FFFFFF | Default component bg |
| `background-color-alt` | #F9F9FA | Hover bg, contrast bg |
| `background-color-alt-2` | #F1F1F3 | Secondary contrast bg |
| `background-color-alt-3` | #E5E6E9 | Tertiary contrast bg |
| `background-color-disabled` | #F1F1F3 | Disabled component bg |
| `background-color-accent` | #0F67FF | Primary button bg |
| `background-color-accent-alt` | #065AEC | Primary button hover |
| `background-color-accent-alt-2` | #024ED3 | Primary button active |
| `background-color-accent-soft` | #F5F9FF | Info alert bg |
| `background-color-danger` | #E3063D | Danger button bg |
| `background-color-danger-soft` | #FFF6F8 | Danger alert bg |
| `background-color-warning` | #F98118 | Warning bg |
| `background-color-warning-soft` | #FFF8F3 | Warning alert bg |
| `background-color-success-soft` | #FDFFEB | Success alert bg |

### Border Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `border-color-base` | #A4A6AF | Default borders |
| `border-color-alt` | #DBDCDF | Subtle borders |
| `border-color-alt-2` | #E5E6E9 | Very subtle borders |
| `border-color-alt-3` | #F1F1F3 | Faintest borders |
| `border-color-accent` | #0F67FF | Active/focus borders |
| `border-color-danger` | #E3063D | Error borders |
| `border-color-success` | #8F9900 | Success borders |

### Fill Colors (Icons)

| Token | Hex | Usage |
|-------|-----|-------|
| `fill-color-accent` | #0F67FF | Info icons |
| `fill-color-danger` | #E3063D | Error icons |
| `fill-color-warning` | #DE6800 | Warning icons |
| `fill-color-success` | #8F9900 | Success icons |

## Colors — Dark Theme (Semantic Tokens)

Key differences from light theme:

| Token | Light | Dark |
|-------|-------|------|
| `text-color-brand` | #050F34 | #F9F9FA |
| `text-color-base` | #31343F | #E5E6E9 |
| `text-color-alt` | #686B76 | #BABCC2 |
| `text-color-accent` | #0F67FF | #74ABFF |
| `text-color-danger` | #E3063D | #FF4D7A |
| `text-color-warning` | #A04B00 | #FF9639 |
| `text-color-success` | #697000 | #CFD94A |
| `background-color-body` | #F9F9FA | #1D202B |
| `background-color-base` | #FFFFFF | #252937 |
| `background-color-alt` | #F9F9FA | #31343F |
| `background-color-alt-2` | #F1F1F3 | #3F424B |

## PRTG Sensor Status Mapping

Recommended mapping of PRTG sensor statuses to Spectrum semantic colors:

| PRTG Status | Spectrum Token | Color |
|-------------|---------------|-------|
| UP | `fill-color-success` / `background-color-success-soft` | Green |
| DOWN | `fill-color-danger` / `background-color-danger-soft` | Red |
| WARNING | `fill-color-warning` / `background-color-warning-soft` | Orange |
| PAUSED | `text-color-disabled` / `background-color-disabled` | Grey |
| UNKNOWN | `text-color-alt` / `background-color-alt-2` | Grey |
