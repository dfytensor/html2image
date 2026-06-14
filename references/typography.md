# Typography for Social Media Carousel

Font selection and text sizing guidelines for carousel images.

---

## Font Pairing Rules

1. Max **2 fonts** per carousel
2. Cross the boundary: serif + sans, display + sans, or sans + mono
3. Body text MUST be a clean sans-serif (readability first)

## Recommended Font Pairs

| Mood | Title Font | Body Font | Notes |
|------|-----------|-----------|-------|
| Warm/lifestyle | Rounded sans (e.g., Nunito, Quicksand) | System sans | Friendly, approachable |
| Knowledge/edu | Serif (e.g., Playfair, Lora) | System sans | Authoritative |
| Bold/social | Heavy sans (e.g., Anton, Impact) | System sans | Punchy, impactful |
| Minimal/editorial | Serif (e.g., Cormorant, EB Garamond) | Mono | Refined, literary |
| Cute/playful | Rounded sans (e.g., Baloo 2) | Rounded sans | Fun, young |
| Premium/luxury | Didone serif (e.g., Playfair Display) | Light sans | Elegant, exclusive |
| Tech/modern | Geometric sans (e.g., Space Grotesk) | Mono | Clean, modern |

## CDN Font Loading

```html
<!-- Google Fonts CDN -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;900&family=Noto+Serif+SC:wght@400;700&display=swap" rel="stylesheet">
```

## Chinese Font Stack

```css
font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
/* Serif */
font-family: "Noto Serif SC", "STSong", "SimSun", serif;
```

## Size Scale

| Element | Size (px) | Weight | Line Height |
|---------|-----------|--------|-------------|
| Cover hero number | 120-200 | 900 | 0.9 |
| Cover title | 64-96 | 700-900 | 1.1 |
| Cover subtitle | 32-44 | 400-500 | 1.3 |
| Page title | 44-64 | 700 | 1.2 |
| Section label | 24-28 | 600 | 1.3 |
| Body text | 26-34 | 400 | 1.7 |
| Caption/muted | 20-24 | 400 | 1.4 |
| Page number | 16-20 | 400 | 1.0 |
| Data big number | 48-72 | 900 | 1.0 |

## Text Emphasis Techniques

| Technique | CSS | Use For |
|-----------|-----|---------|
| Bold | `font-weight: 700` | Key words in body |
| Color | `color: var(--accent)` | Important terms |
| Background strip | `background: rgba(accent, 0.15)` | Definitions |
| Underline | `text-decoration: underline` | Critical points |
| Highlight box | Separate div with background | Key takeaways |
| Size contrast | Larger font-size | Numbers, stats |

## Text Wrapping

```css
/* Prevent awkward line breaks */
max-width: 840px; /* within content area */

/* Chinese text wrapping */
word-break: break-all; /* for mixed CJK/Latin */

/* Prefer max-width over br tags */
/* NEVER use <br> for layout */
```

## BANNED

- Comic Sans, Papyrus, Impact (for body), Curlz MT
- Gradient text (`background-clip: text`)
- Text smaller than 18px
- More than 2 font families on one page
- All-caps body text (titles OK)
- Center-aligned body text (titles and quotes OK)
