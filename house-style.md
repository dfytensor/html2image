# House Style

Default creative direction when no specific visual style is requested.

---

## Design Philosophy

Social media carousel images must be:
1. **Instantly readable** -- Users scroll at speed; each image must communicate in < 2 seconds
2. **Visually consistent** -- All pages in a carousel must look like they belong together
3. **Thumb-friendly** -- Text large enough to read without zooming
4. **Platform-aware** -- Safe zones respected, no critical content near edges

---

## Color Strategy

| Role | Value | Usage |
|---|---|---|
| Background | `#FFF8F0` | Page background (warm cream) |
| Text | `#2D2016` | Body text, titles (dark brown) |
| Accent | `#E8833A` | Highlights, numbers, icons (warm orange) |
| Cards | `#FFFFFF` | Content cards, tip boxes |
| Muted | `#8B7355` | Captions, secondary text |

Rules:
- One background color across all pages
- One accent color -- used sparingly (numbers, icons, key words only)
- Tint neutrals toward your accent (warm gray, not pure gray)
- Declare palette up front; don't invent colors per-page

---

## Background Layer

Every carousel page needs visual depth beyond a flat solid color:

Include 2-4 decorative background elements:
- Soft gradient overlay (subtle, not distracting)
- Corner shape or blob (low opacity, 5-15%)
- Thin decorative line or dot pattern
- Color block accent strip (edge or corner)

Backgrounds should be SUBTLE -- content text must maintain high contrast and readability.

---

## Typography Quick Rules

| Context | Font | Weight | Size |
|---------|------|--------|------|
| Cover title | System sans-serif | 800-900 | 80-120px |
| Cover subtitle | System sans-serif | 400-500 | 36-44px |
| Page title | System sans-serif | 700 | 48-64px |
| Body text | System sans-serif | 400 | 28-36px |
| Caption / label | Monospace or sans | 400 | 20-24px |
| Page number | System sans-serif | 400 | 18-20px |

Minimum sizes for readability:
- Body text: **24px** minimum
- Title: **40px** minimum
- Cover title: **64px** minimum

Font pairing rules:
- Max **2 fonts** per carousel
- Cross the boundary: serif title + sans body, or display title + sans body
- BANNED: Comic Sans, Papyrus, or any decorative font for body text

---

## Layout Principles

### The Safe Zone

```
+------------------------------------------+
|              120px top margin             |
|  +--------------------------------------+|
|  |                                      ||
|  |60px                          60px    ||
|  |  left                        right   ||
|  |                                      ||
|  |         CONTENT AREA                 ||
|  |                                      ||
|  |                                      ||
|  +--------------------------------------+|
|              180px bottom margin          |
+------------------------------------------+
```

ALL text must be within the content area. Only decorative elements may extend beyond.

### Grid System

Use a simple 2-column or 3-column grid within the content area:

**2-column (most common):**
- Left column: 60% (text content)
- Right column: 40% (decorative/visual)

**3-column (for lists/grids):**
- Equal width columns with 20px gutters

### Vertical Rhythm

- Title: 48-64px from top of content area
- Body: 24px below title
- Cards: 32px spacing between cards
- Page indicator: bottom-right of content area

---

## Card Styles

Cards are the primary content container for tips, steps, and data points.

### Standard Card

```css
.card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 32px;
    margin-bottom: 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
```

### Accent Card (with left border)

```css
.card-accent {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 32px;
    border-left: 4px solid var(--accent);
    margin-bottom: 24px;
}
```

### Icon Card (with top icon)

```css
.card-icon {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 32px;
    text-align: center;
    margin-bottom: 24px;
}
.card-icon .icon {
    width: 64px;
    height: 64px;
    margin: 0 auto 16px;
}
```

---

## Page Indicator Styles

```css
.page-indicator {
    position: absolute;
    bottom: 24px;
    right: 24px;
    font-size: 18px;
    color: rgba(0,0,0,0.3);
}
.page-indicator .current {
    color: var(--accent);
    font-weight: 700;
}
```

---

## Decorative Elements

### Wavy Divider

```html
<svg viewBox="0 0 960 40" style="width:100%;opacity:0.15">
  <path d="M0,20 Q120,0 240,20 Q360,40 480,20 Q600,0 720,20 Q840,40 960,20" fill="none" stroke="currentColor" stroke-width="2"/>
</svg>
```

### Dot Pattern

```css
.dots {
    background-image: radial-gradient(circle, var(--accent) 1px, transparent 1px);
    background-size: 24px 24px;
    opacity: 0.08;
}
```

### Corner Blob

```css
.blob-tr {
    position: absolute;
    top: -60px;
    right: -60px;
    width: 240px;
    height: 240px;
    background: var(--accent);
    border-radius: 50%;
    opacity: 0.08;
    filter: blur(40px);
}
```

---

## Icon Rules

- No emoji -- use SVG icons or icon fonts
- Recommended: Remix Icon (wide coverage) or Lucide (clean modern)
- Icon size: 32-64px for inline, 80-120px for feature icons
- Match icon color to accent palette

CDN links:
```html
<link href="https://cdn.jsdelivr.net/npm/remixicon@4.2.0/fonts/remixicon.css" rel="stylesheet">
```

---

## Palettes

| Category | File |
|----------|------|
| Warm / Lifestyle | [palettes/warm-lifestyle.md](palettes/warm-lifestyle.md) |
| Pastel / Soft | [palettes/pastel-soft.md](palettes/pastel-soft.md) |
| Bold / Social | [palettes/bold-social.md](palettes/bold-social.md) |
| Clean / Knowledge | [palettes/clean-knowledge.md](palettes/clean-knowledge.md) |
| Dark / Aesthetic | [palettes/dark-aesthetic.md](palettes/dark-aesthetic.md) |
| Nature / Fresh | [palettes/nature-fresh.md](palettes/nature-fresh.md) |
| Minimal / Mono | [palettes/minimal-mono.md](palettes/minimal-mono.md) |
