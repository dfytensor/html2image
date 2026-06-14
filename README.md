# html2image

A skill-based toolkit for converting text content into polished social media carousel images. Write HTML slides using provided design patterns and palettes, then render them to pixel-perfect PNGs via Playwright — optimized for Xiaohongshu, Instagram, WeChat, and more.

## Features

- **Dual-size output from one HTML** — Portrait (1080x1440) and Landscape (1024x436) from a single responsive file using CSS custom properties
- **9 layout patterns** — Cover, text-heavy, tip card, quote, split, step flow, checklist, data card, summary/CTA, plus version comparison and Apple-style poster
- **7 named visual styles** — Warm Lifestyle, Clean Knowledge, Bold Social, Pastel Soft, Dark Aesthetic, Nature Fresh, Minimal Mono
- **Platform safe zones** — Built-in margins for platform UI overlays (headers, navigation bars)
- **Remix Icons integration** — Vector icon system on every data card, label, and checklist
- **Post caption generation** — Auto-generates social media caption text alongside images

## Quick Start

### Prerequisites

```bash
pip install playwright pillow
playwright install chromium
```

### Basic Usage

```bash
# Portrait (1080x1440) — Xiaohongshu / Instagram Portrait
python scripts/html2carousel.py input.html -o output/ --caption

# Landscape (1024x436) — WeChat cover / banner
python scripts/html2carousel.py input.html -o output/ --width 1024 --height 436 --prefix cover_1024x436
```

### Full Example (Dual-Size)

```bash
# Step 1: Render portrait
python scripts/html2carousel.py my_carousel.html -o output/ --width 1080 --height 1440 --prefix carousel --caption

# Step 2: Render landscape (same HTML)
python scripts/html2carousel.py my_carousel.html -o output/ --width 1024 --height 436 --prefix cover_1024x436
```

Output:

```
output/
  carousel_001.png        # Portrait page 1
  carousel_002.png        # Portrait page 2
  ...
  cover_1024x436_001.png  # Landscape page 1
  cover_1024x436_002.png  # Landscape page 2
  ...
  _post_text.txt          # Auto-generated social media caption
```

## How It Works

```
Text content (story / blog / tips / report)
        |
        v
  Write HTML carousel          <-- Use patterns from references/
  (responsive, dual-size)          and palettes from palettes/
        |
        v
  html2carousel.py             <-- Playwright screenshots
  Run 1: 1080x1440                 each .slide element
  Run 2: 1024x436
        |
        v
  PNG images ready to post
```

### Responsive HTML Pattern

A single HTML file renders at both sizes via CSS variables:

```html
<style>
  :root {
    --safe-top: 120px;
    --fs-page-title: 48px;
    /* portrait defaults */
  }

  /* Landscape overrides */
  @media (max-height: 600px) {
    :root {
      --safe-top: 24px;
      --fs-page-title: 26px;
    }
    .slide { width: 1024px; height: 436px; }
  }
</style>
```

## Project Structure

```
html2image/
  SKILL.md                        Skill definition: rules, gates, phases, layout specs
  visual-styles.md                7 named visual styles with color tables
  house-style.md                  Default design philosophy and typography rules
  scripts/
    html2carousel.py              HTML → PNG converter (Playwright-based)
  palettes/
    warm-lifestyle.md             Warm cream + orange (food, wellness, lifestyle)
    clean-knowledge.md            Cool gray + blue (education, tech, science)
    bold-social.md                Vibrant orange/yellow (fitness, motivation)
    pastel-soft.md                Soft pink/lavender (beauty, fashion, gentle)
    dark-aesthetic.md             Near-black + crimson/gold (luxury, mood)
    nature-fresh.md               Green/natural (eco, outdoors, health)
    minimal-mono.md               Monochrome minimal (editorial, professional)
  references/
    carousel-patterns.md          10+ ready-to-use HTML/CSS layout templates
    typography.md                 Font sizing, spacing, and readability rules
  assets/
    templates/
      demo-sleep-tips.html        Working demo: 6-page sleep tips carousel
```

## Layout Patterns

| Pattern | Best For | Key Feature |
|---------|----------|-------------|
| Cover Card | Page 1 hook | Large title, visual punch, swipe hint |
| Text-Heavy | Explanations | Generous text area with decorative elements |
| Tip Card | List items | Numbered card with icon and short text |
| Quote Card | Key statements | Large centered text with decorative frame |
| Split Comparison | Before/after | Two-column contrast layout |
| Step Flow | Tutorials | Numbered steps with visual connectors |
| Checklist | Habits, to-do | Checkbox-style list items |
| Data Card | Stats, metrics | Big number + supporting label |
| Version Comparison | Multi-model eval | Row cards with icon badges + values |
| Summary/CTA | Last page | Key takeaway + follow prompt |
| Apple-style Poster | Infographic poster | Pure black bg, ultra-thin dividers, bar chart |

See [references/carousel-patterns.md](references/carousel-patterns.md) for full HTML/CSS code.

## Platform Resolutions

| Platform | Resolution | Aspect Ratio |
|----------|-----------|--------------|
| Xiaohongshu (portrait) | 1080x1440 | 3:4 |
| Xiaohongshu (square) | 1080x1080 | 1:1 |
| WeChat Article cover | 1024x436 | ~2.35:1 |
| Instagram Feed | 1080x1080 | 1:1 |
| Instagram Portrait | 1080x1350 | 4:5 |
| Instagram Story | 1080x1920 | 9:16 |

## CLI Options

```
python scripts/html2carousel.py <input.html> [options]

  -o, --output <dir>        Output directory (default: ./carousel_output/)
  --width <px>              Image width (default: 1080)
  --height <px>             Image height (default: 1440)
  --slide-selector <css>    CSS selector for slides (default: .slide)
  --format <png|jpg>        Output format (default: png)
  --quality <1-100>         JPG quality (default: 95)
  --prefix <name>           Filename prefix (default: carousel)
  --caption                 Generate _post_text.txt caption file
  --platform <platform>     Target platform tag (default: xiaohongshu)
```

## License

MIT
