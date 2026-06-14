---
name: carousel-image
description: |
  Convert text content (stories, blogs, tips, knowledge) into multi-image carousel
  for social media platforms like Xiaohongshu (Little Red Book), WeChat, Instagram, etc.
  Triggered when user wants to create carousel posts, image slides, story strips,
  or any multi-page image content for social sharing.
  Trigger phrases: "generate carousel", "multi-image", "slides for posting",
  "小红书图文", "轮播图", "多图", "信息图", "图文笔记", "story slides",
  "Instagram carousel", "WeChat post images".
  Pipeline: text -> carousel design -> HTML rendering -> PNG images.
---

# Carousel Image Skill

Convert text content into multi-image carousel for social media platforms.

---

## Pipeline Overview

```
User provides text content (story/blog/tips/knowledge)
        |
        v
  Phase 1: Carousel Planning
     Determine page count, layout per page, text distribution
     Output: _carousel_design.json
        |
        v
  Phase 2: Generate HTML Carousel
     Mode A (default): AI generates ONE responsive HTML that works at both sizes
       Portrait (1080x1440) + Landscape (1024x436) -- same HTML, two render passes
     Mode B: User provides images -> AI adds text overlay -> composite
        |
        v
  Phase 3: HTML -> Images (dual-size output by default)
     Run 1: Portrait screenshots (1080x1440) -> carousel_001.png, ...
     Run 2: Same HTML at 1024x436 -> cover_1024x436_001.png, ...
     Both runs output ALL pages
        |
        v
  Optional Phase 4: Post Text Generation
     Generate social media caption, hashtags, posting text
     Output: _post_text.txt
```

---

## Visual Identity Gate

<HARD-GATE>
Before writing ANY HTML, you MUST have a visual identity defined.

Check in this order:

1. **User specified a style?** -> Read [visual-styles.md](visual-styles.md) for named styles (Warm Lifestyle, Clean Knowledge, Bold Social, Dark Aesthetic, etc.).
2. **Content naturally fits a style?** -> Use the Style Selection Matrix in [visual-styles.md](visual-styles.md) to pick the best match.
3. **None of the above?** -> Ask the user:
   - What's the mood? (lifestyle / knowledge / emotional / dramatic / cute)
   - Light or dark background?
   - Any brand colors or visual references?
</HARD-GATE>

---

## <HARD-GATE> Before Generating HTML

1. **No emoji** -- Replace with vector UI icons or decorative SVG elements.
2. **Text must be image-safe** -- Minimum body 20px, titles 36px, all text high contrast.
3. **No animation needed** -- Carousel images are static. No GSAP, no CSS animation. Focus on layout and typography.
4. **Content density** -- Each image should have 1 clear focal point. Don't overload a single image.
5. **Consistent visual language** -- Same palette, font, and decorative elements across all images in one carousel.

---

## Image Specifications

### Platform Defaults

| Platform | Resolution | Aspect Ratio | Max Images | Notes |
|----------|-----------|--------------|------------|-------|
| Xiaohongshu | 1080x1440 | 3:4 | 18 | Portrait, lifestyle/knowledge |
| Xiaohongshu (square) | 1080x1080 | 1:1 | 18 | Square format |
| WeChat Article | 900x383 | 2.35:1 | N/A | Cover only |
| WeChat Moments | 1080x1080 | 1:1 | 9 | Square or 3:4 |
| Instagram Feed | 1080x1080 | 1:1 | 10 | Square |
| Instagram Portrait | 1080x1350 | 4:5 | 10 | Portrait |
| Instagram Story | 1080x1920 | 9:16 | N/A | Full portrait |
| General | 1080x1440 | 3:4 | -- | Default if not specified |

**Default:** 1080x1440 (3:4 portrait, Xiaohongshu style)

### Text Safety Zones

All text must stay within safe zones to account for platform UI overlays:

| Edge | Safe Margin |
|------|------------|
| Top | 120px (platform header, time, signal) |
| Bottom | 180px (navigation bar, likes, comments) |
| Left | 60px |
| Right | 60px |

**Content area:** Inner rectangle with these margins applied.

---

## Phase 1: Carousel Planning

<HARD-GATE>
Before generating HTML, plan the carousel structure. This ensures coherent storytelling and proper text distribution.
</HARD-GATE>

### Planning Steps

1. **Determine page count** -- Based on content length and type:
   - Tips/list: 1 cover + N tip pages + 1 summary = typically 6-12 pages
   - Story/narrative: 1 cover + story pages + 1 ending = typically 8-15 pages
   - Knowledge/explain: 1 cover + concept pages + 1 summary = typically 6-10 pages
   - Emotional/quote: 1 cover + quote pages + 1 CTA = typically 5-8 pages

2. **Assign layout per page** -- Each page gets a layout type from the pattern catalog:

| Page Position | Recommended Layout | Purpose |
|--------------|-------------------|---------|
| Page 1 (Cover) | Cover Card | Hook title, visual impact, curiosity gap |
| Page 2 | Topic Intro | Explain what this carousel is about |
| Page 3-N | Content pages | Tips, steps, story beats, knowledge points |
| Last page | Summary/CTA | Key takeaway, follow CTA, or emotional ending |

3. **Distribute text** -- Split content across pages:
   - Each page: 1 main point + supporting details
   - Max 100 characters Chinese per page body text (readability)
   - Max 15 characters for main title per page
   - Keep related content together (don't split a step across pages)

4. **Assign visual style** -- Select from visual-styles.md

### Output: _carousel_design.json

```json
{
  "project": "5 Tips for Better Sleep",
  "platform": "xiaohongshu",
  "resolution": { "width": 1080, "height": 1440 },
  "total_pages": 8,
  "style": "warm-lifestyle",
  "palette": {
    "bg": "#FFF8F0",
    "fg": "#2D2016",
    "accent": "#E8833A",
    "card": "#FFFFFF",
    "muted": "#8B7355"
  },
  "pages": [
    {
      "index": 0,
      "layout": "cover",
      "title": "5个睡眠秘诀",
      "subtitle": "让你每天精神百倍",
      "visual_note": "Oversized number 5, warm gradient background",
      "body": ""
    },
    {
      "index": 1,
      "layout": "text-heavy",
      "title": "为什么睡不好？",
      "body": "80%的睡眠问题来自这5个坏习惯...",
      "visual_note": "Problem statement with icon"
    },
    {
      "index": 2,
      "layout": "tip-card",
      "title": "秘诀一",
      "subtitle": "固定作息时间",
      "body": "每天同一时间入睡和起床，即使周末也不例外。你的生物钟会感谢你。",
      "visual_note": "Clock icon + numbered card"
    }
  ]
}
```

---

## Phase 2: Generate HTML Carousel

### Mode A: AI-Generated HTML (Default)

**Trigger:** User provides content and wants carousel images.

#### HTML Structure Requirements

Every carousel HTML must follow this structure. **Layout must work at both 1080x1440 AND 1024x436.**

Use CSS custom properties for ALL sizes, with `@media (max-height: 600px)` overrides for landscape.

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <style>
    :root {
      --bg: #F8F9FA;
      --fg: #1A1A2E;
      --accent: #0984E3;
      --card: #FFFFFF;
      --muted: #6C7A89;
      --surface: #E8F4FD;
      --safe-top: 120px;
      --safe-bottom: 180px;
      --safe-side: 60px;
      --fs-page-title: 48px;
      --fs-body: 30px;
      --fs-label: 24px;
      --fs-caption: 20px;
      --fs-data-lg: 44px;
      --radius-card: 16px;
      --pad-card: 24px 28px;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: var(--bg); font-family: "Noto Sans SC", sans-serif; }
    .carousel { width: 1080px; }
    .slide {
      width: 1080px; height: 1440px;
      position: relative; overflow: hidden; page-break-after: always;
    }
    .content {
      position: absolute;
      top: var(--safe-top); left: var(--safe-side);
      right: var(--safe-side); bottom: var(--safe-bottom);
      display: flex; flex-direction: column;
    }

    /* Landscape overrides */
    @media (max-height: 600px) {
      :root {
        --safe-top: 24px; --safe-bottom: 24px; --safe-side: 40px;
        --fs-page-title: 26px; --fs-body: 16px;
        --fs-label: 14px; --fs-caption: 12px;
        --fs-data-lg: 28px; --radius-card: 10px; --pad-card: 10px 14px;
      }
      .carousel { width: 1024px; }
      .slide { width: 1024px; height: 436px; }
    }
  </style>
</head>
<body>
  <div class="carousel">
    <div class="slide" id="slide-0"> ... </div>
    <div class="slide" id="slide-1"> ... </div>
    <!-- more slides -->
  </div>
</body>
</html>
```

#### Layout Templates

Each slide uses one of these layout types. Read [references/carousel-patterns.md](references/carousel-patterns.md) for full HTML/CSS code.

| Layout | Best For | Key Feature |
|--------|----------|-------------|
| **Cover Card** | Page 1 hook | Large title, visual punch, page indicator |
| **Text-Heavy** | Explanations, paragraphs | Generous text area with decorative elements |
| **Tip Card** | List items, tips | Numbered card with icon and short text |
| **Quote Card** | Key statements, emotions | Large centered text with decorative frame |
| **Split Image** | Before/after, comparison | Text left/right, image area on opposite side |
| **Step Flow** | Tutorials, processes | Numbered steps with visual connectors |
| **Checklist** | To-do, habits | Checkbox-style list items |
| **Summary/CTA** | Last page | Key takeaway + follow prompt |
| **Data Card** | Stats, comparisons | Big number + supporting text |

#### Page Indicator

Every page (except cover) must include a page indicator:

```html
<div class="page-indicator">
  <span class="current">3</span>
  <span class="separator">/</span>
  <span class="total">8</span>
</div>
```

Position: bottom-right of safe zone. Style: small, muted color, does not distract from content.

#### Cover Page Requirements

The cover (Page 1) is the most critical -- it determines whether users swipe.

<HARD-GATE>
Cover page MUST satisfy ALL of these:
1. **Hook title** -- Creates curiosity, uses one of the hook patterns below
2. **Visual punch** -- Oversized number, bold color block, or dramatic contrast
3. **Platform-appropriate** -- No text in danger zones, clear at thumbnail size
4. **No page indicator** -- Cover does not show "1/8"
5. **Swipe hint** -- Subtle visual cue to encourage swiping (arrow, dots)
</HARD-GATE>

**Hook Title Patterns for Social Media Carousel:**

| # | Pattern | Title | Subtitle |
|---|---------|-------|----------|
| 1 | Number list | "5个改变人生的习惯" | "第3个你一定没想到" |
| 2 | Shock stat | "90%的人不知道这个技巧" | "学会了效率翻倍" |
| 3 | Question | "为什么你总是觉得累？" | "答案可能出乎意料" |
| 4 | Before/after | "从月入3千到年入百万" | "他只做对了这一件事" |
| 5 | Challenge | "你坚持不了7天" | "试试这个方法" |
| 6 | Secret reveal | "医生不会告诉你的秘密" | "关于睡眠的真相" |
| 7 | How-to | "3步搞定完美早餐" | "零失败食谱" |
| 8 | Story teaser | "那年夏天，我差点放弃" | "一个关于勇气的故事" |
| 9 | Comparison | "月薪3千 vs 月薪3万" | "差距到底在哪？" |
| 10 | Promise | "看完这篇，你就不焦虑了" | "5个心理学小技巧" |

**BANNED cover patterns:**
- "XXX分享" / "XXX介绍" / "XXX总结" (boring, no curiosity)
- Plain centered text on solid background (no visual punch)
- Too much text on cover (max title + subtitle, no body text)

---

## Page-Level Hook System (Swiper's Journey)

The 10 cover hook patterns above govern **Page 1 only**. This section governs **every page after** -- ensuring each page has a narrative function, each swipe creates momentum, and the user never thinks "why am I still swiping?"

### Why Carousel Hooks Are Different From Video Hooks

Video: viewer passively watches. Time passes automatically.
Carousel: **viewer actively decides** to swipe each page. No swipe = abandoned.

Every page transition is a **micro-decision point**. The user's thumb hovers: "swipe or close?" Each page must earn the next swipe.

---

### Six Carousel Hook Types

Adapted from the video narrative-hook-adapter for social media carousel context:

| Hook Type | Code | Core Emotion | Carousel Example |
|-----------|------|-------------|------------------|
| **Surprising Stat** | STAT | Shock + exclusion | "Most people think 8 hours is enough -- it's not" |
| **Counterintuitive** | COUNTER | Cognitive dissonance | "Sleeping MORE can make you MORE tired" |
| **Hidden Mechanism** | MYSTERY | Curiosity + discovery | "The real secret isn't what you do -- it's WHEN you do it" |
| **Direct Challenge** | CHALLENGE | Challenge + social proof | "Can you stick to this for 7 days? 90% can't" |
| **Result Reveal** | RESULT | Surprise + payoff | "After 21 days, this happened..." |
| **Future Promise** | PROMISE | Aspiration + FOMO | "The last tip is the one that changed everything" |

---

### Hook Density Rules (Per Carousel)

<HARD-GATE>
Every carousel with 5+ pages MUST satisfy ALL three density requirements. Carousels with fewer than 5 pages must still satisfy the opening and closing hook requirements.
</HARD-GATE>

| Position | Requirement | Page Range | Minimum |
|----------|-------------|-----------|---------|
| **Opening Hook** | Page 1 (Cover) | Page 1 | 1 hook |
| **Mid-Carousel Hook** | A page in the 40-60% range that raises stakes or reveals a twist | Middle pages | 1 hook per 4-5 pages |
| **Closing Hook** | Final page ends with forward-looking hook (PROMISE or MYSTERY) | Last page | 1 hook |

**Mid-Carousel Hook Examples:**

| Situation | Mid-Hook Pattern | Implementation |
|-----------|-----------------|----------------|
| Tips list | "But here's the one nobody talks about..." | Reveal unexpected tip at 50% mark |
| Knowledge explain | "This is where most people get it wrong" | Show common misconception before truth |
| Story | "And then everything changed..." | Plot twist at midpoint |
| Comparison | "You might think A is better. The data says otherwise" | Challenge assumption |

---

### Inter-Page Hook Propagation (Swipe Motivation Chain)

Pages are not isolated -- they form a **hook propagation chain**. Each page (except the last) must plant a reason to swipe forward.

```
Page 1: Opening Hook A → Half-Result A + Swipe Hook B
Page 2: Hook B (resolves A's tension) → Full Content + Swipe Hook C
Page 3: Hook C → Half-Result C + Swipe Hook D
...
Page N: Hook X → Full Result (payoff) + PROMISE hook (follow/like/save)
```

**Inter-page hook implementation techniques:**

| Technique | How | Carousel Example |
|-----------|-----|------------------|
| **Cliffhanger text** | End a page with an unfinished sentence or "but..." | "...但这还不是最离谱的。左滑看真相 →" |
| **Preview tease** | Show a blurred/obscured preview of next page's content | Grayed-out card with "下一个秘诀是..." |
| **Question bridge** | Ask a question at bottom of page, answer on next page | "你知道哪个习惯最伤睡眠吗？" → Next page reveals it |
| **Contrast setup** | Present "before" state, promise "after" on next page | "这是改变前..." → Next: "这是改变后" |
| **Number tease** | Reference a specific upcoming page number | "第4个秘诀才是关键，记得滑到最后" |
| **Visual arrow** | Explicit directional cue (arrow icon, swipe hint) at bottom | "→ 左滑继续" with accent arrow |
| **Half-result** | Resolve question A but reveal bigger question B | "解决了入睡问题——但怎么保证睡得深？" |

**BANNED inter-page patterns:**
- Nothing at the bottom of a page (dead end = user closes)
- "接下来看..." / "下面介绍..." (boring, no tension)
- Same phrase repeated on every page (feels mechanical)
- No swipe cue of any kind (user doesn't know there's more)

---

### Half-Result Hook Design (Between Pages)

The most powerful swipe motivator. Resolve one curiosity but open a bigger one:

| Pattern | How It Works | Carousel Example |
|---------|-------------|------------------|
| **Answer half, ask more** | Resolve question A but reveal bigger question B | "固定作息解决了入睡——但为什么还是睡不深？→" |
| **False resolution** | Seemingly solved, but a trap | "不看手机就行了？其实手机不是最大的问题 →" |
| **Cost resolution** | Solved but at a price | "20度室温确实有效——但冬天很难做到 →" |
| **Perspective flip** | Resolved from one angle, new crisis from another | "从入睡角度看，没问题了。从深度睡眠角度看... →" |
| **Time lock** | Resolved but sets new constraint | "方法有效——但需要坚持21天 →" |
| **Ranking tease** | "This was good, but the NEXT one is even better" | "秘诀3不错，但秘诀4才是真正的game changer →" |

---

### Three-Act Carousel Structure (起因→经过→结果)

<HARD-GATE>
Carousels with 6+ pages MUST follow the three-act structure. The proportion is a guideline (+-10%). What matters is that each act's PURPOSE is fulfilled.
</HARD-GATE>

| Act | Proportion | Purpose | Pages | Hook Requirement |
|-----|-----------|---------|-------|-----------------|
| **起因 (Setup)** | ~20-25% | Hook + problem + context | Pages 1-2 | Opening hook (Page 1) + problem framing (Page 2) |
| **经过 (Development)** | ~45-55% | Content delivery + escalating interest + mid-hook | Pages 3 to N-2 | Mid-escalation hook at peak page |
| **结果 (Result)** | ~20-25% | Resolution + payoff + CTA | Last 1-2 pages | Closing PROMISE/MYSTERY hook |

#### Act 1 -- 起因 (Setup, ~20-25%)

| Page | Function | Content | Hook Role |
|------|----------|---------|-----------|
| Page 1 | Hook cover | Visual punch + hook title + tension subtitle | Cover hook (existing rules) |
| Page 2 | Problem reveal | Answer the cover's hook / reveal the problem / define scope | Resolve Page 1 hook, plant Page 3 curiosity |

**Narrative arc:** "Something surprising/important" → "Here's why it matters to you"

#### Act 2 -- 经过 (Development, ~45-55%)

This is the core content. But it must maintain swiping momentum.

| Technique | Purpose | When to Use |
|-----------|---------|-------------|
| **Interest escalation** | Each page raises the stakes or reveals more | Tips go from common to surprising |
| **Mid-carousel hook** | A surprise/twist at the 50-60% mark | "But the REAL game-changer is..." |
| **Pattern interruption** | Break the layout rhythm to re-engage | Insert a Quote Card among Tip Cards |
| **Progressive specificity** | Start general, get increasingly specific | Overview → details → surprising nuance |

**Development page ordering principles:**
1. Start with what the viewer already knows (familiar ground)
2. Build toward what they don't know (new insight)
3. Insert mid-escalation hook when interest might dip
4. End Act 2 with setup for the Act 3 payoff

#### Act 3 -- 结果 (Result, ~20-25%)

| Page | Function | Content | Hook Role |
|------|----------|---------|-----------|
| N-1 | Payoff | Best result / summary / "the answer" | Full resolution of all major hooks |
| N | Forward hook | CTA / recommendations / emotional ending | Closing PROMISE or MYSTERY hook |

**Result page MUST:**
1. Pay off the opening hook's promise (if Page 1 asked a question, answer it here)
2. Show the "after" to contrast with Page 2's "before"
3. End with forward-looking hook: PROMISE ("关注我，下期更精彩") or MYSTERY ("还有一个秘密没说...")

---

### Hook Strength Curve

The narrative-hook-adapter uses a 1-5 strength scale. Apply this to carousel:

| Strength | Level | Carousel Equivalent | Example |
|----------|-------|-------------------|---------|
| 1 | Background tension | Color shift, visual hint of importance | Slightly different card style |
| 2 | Mild curiosity | A detail that stands out | "你可能没注意过这个..." |
| 3 | Active curiosity | An explicit question or partial reveal | "你觉得哪个习惯最伤睡眠？" |
| 4 | Strong pull | Counterintuitive result or dramatic contrast | "你一直在做错的3件事" |
| 5 | Must-see reveal | Peak moment that recontextualizes everything | "而第5个秘诀，颠覆了所有人的认知" |

**Strength curve rules:**

1. Alternate strong and weak hooks -- don't put all 5s together (swipe fatigue)
2. Every 3-4 pages, insert at least one strength-4 or strength-5 hook
3. The **strongest hook** must be either the opening (Page 1) or the mid-escalation point
4. The **final page's** hook should be strength 3-4 (PROMISE/MYSTERY), not 5 (save the ultimate payoff for content, not the tease)
5. Strength curve should form a rough "W" shape: High opening → dip → mid-escalation peak → dip → strong closing

```
Strength
  5 |   *                           *
  4 |          *              *
  3 |                    *              *
  2 |       *
  1 |
     +--+--+--+--+--+--+--+--+--+--+--→ Pages
      P1 P2 P3 P4 P5 P6 P7 P8 P9
      ↑        ↑              ↑
   Opening  Mid-escalation  Closing
   (STAT)   (COUNTER)       (PROMISE)
```

---

### Carousel Storyboard Planning Table (CT1)

Complete this BEFORE generating HTML:

| Page | Act | Title | Hook Type | Swipe Forward | Strength |
|------|-----|-------|-----------|---------------|----------|
| 1 | 起因 | "5个睡眠秘诀" | STAT | Question: "为什么你总是睡不好？" | 5 |
| 2 | 起因 | "为什么睡不好？" | CHALLENGE | Contrast: "但第1个秘诀就够颠覆了" | 3 |
| 3 | 经过 | "秘诀1: 固定作息" | -- | Tease: "第2个更反直觉" | 2 |
| 4 | 经过 | "秘诀2: 远离手机" | COUNTER | Half-result: "解决了入睡，但深度睡眠呢？" | 4 |
| 5 | 经过 | "秘诀3: 室温20度" | -- | Preview: "后面还有2个" | 2 |
| 6 | 结果 | "秘诀4+5: 完整方案" | RESULT | Full payoff: "这就是完整方案" | 5 |
| 7 | 结果 | "今晚开始" | PROMISE | Forward: "关注我，下期讲晨间习惯" | 3 |

### Carousel Hook Verification Table (CT2)

Complete after planning, before writing HTML:

| Verification Item | Status | Evidence |
|-------------------|--------|----------|
| Three-act structure present (起因/经过/结果) | Y/N | Pages 1-2 (起因), 3-5 (经过), 6-7 (结果) |
| Opening hook (Page 1) | Y/N | STAT hook on cover |
| Mid-escalation hook (40-60%) | Y/N | COUNTER at Page 4 (57%) |
| Closing hook (last page) | Y/N | PROMISE at Page 7 |
| Hook propagation chain intact | Y/N | Every page has swipe-forward element |
| Half-result hooks present | Y/N | P4→P5 half-result |
| Hook strength curve follows W-shape | Y/N | 5-3-2-4-2-5-3 |
| No dead-end pages | Y/N | All pages motivate swiping except last |
| At least 3 different hook types used | Y/N | STAT, COUNTER, CHALLENGE, RESULT, PROMISE |
| Cover withholds the answer | Y/N | Viewer must swipe to resolve |

---

### Enhanced _carousel_design.json (With Hooks)

The carousel design JSON now includes hook metadata per page:

```json
{
  "pages": [
    {
      "index": 0,
      "layout": "cover",
      "title": "5个睡眠秘诀",
      "subtitle": "让你每天精神百倍",
      "hook_type": "STAT",
      "hook_role": "opening",
      "swipe_forward": "为什么你总是睡不好？",
      "strength": 5,
      "act": "起因"
    },
    {
      "index": 1,
      "layout": "text-heavy",
      "title": "为什么睡不好？",
      "body": "80%的睡眠问题来自这5个坏习惯...",
      "hook_type": "CHALLENGE",
      "hook_role": "problem_framing",
      "swipe_forward": "但第1个秘诀就够颠覆了",
      "strength": 3,
      "act": "起因"
    },
    {
      "index": 2,
      "layout": "tip-card",
      "title": "固定作息时间",
      "body": "每天同一时间...",
      "hook_type": null,
      "hook_role": null,
      "swipe_forward": "第2个秘诀更反直觉 →",
      "strength": 2,
      "act": "经过"
    },
    {
      "index": 3,
      "layout": "tip-card",
      "title": "睡前远离手机",
      "body": "睡前1小时...",
      "hook_type": "COUNTER",
      "hook_role": "mid_escalation",
      "swipe_forward": "解决了入睡——但怎么保证深度睡眠？",
      "strength": 4,
      "act": "经过"
    }
  ]
}
```

**New fields explained:**

| Field | Required | Values | Description |
|-------|----------|--------|-------------|
| `hook_type` | On hook pages | STAT, COUNTER, MYSTERY, CHALLENGE, RESULT, PROMISE, null | Hook type for this page |
| `hook_role` | On hook pages | opening, problem_framing, mid_escalation, development, payoff, closing | This page's role in the hook chain |
| `swipe_forward` | Yes (all except last page) | Free text (1-2 sentences) | The curiosity gap / half-result / bridge planted at bottom of this page |
| `strength` | Yes | 1-5 | Hook strength (1=background, 5=must-see) |
| `act` | Yes | 起因 / 经过 / 结果 | Which act this page belongs to |

---

### Swipe Forward Implementation in HTML

Every content page (except last) MUST have a visible swipe-forward element at the bottom of the content area:

```html
<div class="swipe-forward">
  <span class="swipe-text">第2个秘诀更反直觉</span>
  <i class="ri-arrow-right-s-line"></i>
</div>
```

```css
.swipe-forward {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  margin-top: auto;
  padding-top: 20px;
  font-size: 20px;
  color: var(--accent);
  font-weight: 500;
}
```

**Position:** Bottom of the content area (inside safe zone), right-aligned.
**Style:** Accent color, smaller than body text, with arrow icon.
**Content:** Use the `swipe_forward` field from the design JSON.

---

### Hook Quality Checklist (Per Carousel)

Before finalizing any carousel, verify ALL of these:

| # | Question | Pass Criteria |
|---|----------|---------------|
| 1 | Does the cover create a "I need to see more" feeling? | Uses one of 10 hook patterns, not a description |
| 2 | Does every page (except last) motivate swiping? | Has visible swipe-forward element |
| 3 | Is there a mid-carousel hook (40-60%)? | At least one STAT/COUNTER/MYSTERY/CHALLENGE page |
| 4 | Does the last page end with forward motivation? | PROMISE or MYSTERY hook for follow/like |
| 5 | Is the hook propagation chain intact? | Every page resolves previous + plants next |
| 6 | Does the cover withhold the answer? | Viewer must swipe 2+ pages to resolve curiosity |
| 7 | Is the hook strength curve W-shaped? | Not flat, not all-max, varied intensity |
| 8 | Are there at least 3 different hook types? | Don't use the same hook type on every page |
| 9 | Is there at least one half-result hook? | Resolves A but opens B, between pages |
| 10 | Does Act 3 pay off Act 1's hook? | Opening question → answered in result pages |

#### Text Typography Rules

| Element | Min Size | Recommended | Weight | Notes |
|---------|----------|-------------|--------|-------|
| Cover title | 64px | 80-120px | 700-900 | Impact, readable at thumbnail |
| Cover subtitle | 32px | 36-44px | 400-600 | Supporting the hook |
| Page title | 40px | 48-64px | 700 | Clear, scannable |
| Body text | 24px | 28-36px | 400 | Comfortable reading |
| Caption/label | 18px | 20-24px | 400 | Metadata, sources |
| Page number | 16px | 18-20px | 400 | Muted, non-distracting |

**Font pairing:**
- Use at most 2 fonts per carousel
- Cross the boundary: serif title + sans body, or display title + sans body
- NO: two similar sans-serif fonts together

---

### Mode B: User Images + Text Overlay

**Trigger:** User says "add text to my images" or provides existing images.

Pipeline:
1. User provides images (paths or folder)
2. AI designs text overlay layout per image
3. Script composites text onto images using Pillow
4. Output: images with text overlay

This mode uses the script directly:
```bash
python scripts/html2carousel.py --images-dir ./my_photos/ --overlay-text _carousel_design.json -o output/
```

---

## Phase 3: HTML -> Images

### Default: Dual-Size Output

<HARD-GATE>
By default, the pipeline MUST produce TWO versions of ALL pages:

1. **Portrait** (1080x1440, 3:4) -- All pages for social media swiping
2. **Landscape** (1024x436) -- All pages for article thumbnails, WeChat, blog headers

This requires running the script TWICE: once at 1080x1440, once at 1024x436.
The landscape version uses the SAME HTML file -- the script just renders at a different resolution.
Both versions output the same number of pages (carousel_001..carousel_N + cover_1024x436_001..cover_1024x436_N).
</HARD-GATE>

### Script

```bash
# Run 1: Full carousel (portrait, all pages)
python scripts/html2carousel.py input.html -o output/ --caption

# Run 2: Same carousel (landscape, all pages)
python scripts/html2carousel.py input.html -o output/ --width 1024 --height 436 --prefix cover_1024x436
```

### Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `input` | (required) | Input HTML file path |
| `-o` / `--output` | `./carousel_output/` | Output directory for PNG images |
| `--width` | 1080 | Image width |
| `--height` | 1440 | Image height |
| `--slide-selector` | `.slide` | CSS selector for slide elements |
| `--format` | `png` | Output format: png or jpg |
| `--quality` | 95 | JPG quality (1-100) |
| `--prefix` | `carousel` | Filename prefix for output images |
| `--json` | (none) | Path to _carousel_design.json for metadata |
| `--caption` | (off) | Also generate _post_text.txt with social media caption |

### Mode B Parameters (Image + Text Overlay)

| Parameter | Description |
|-----------|-------------|
| `--images-dir` | Directory containing source images |
| `--overlay-text` | Path to _carousel_design.json with text content per page |
| `--font` | Font path for text overlay (default: system font) |

### Landscape Version (1024x436) Design Rules

All pages are rendered at BOTH sizes from the SAME HTML file. The HTML layout must work at both aspect ratios:

| Version | Resolution | Aspect | Use Case |
|---------|-----------|--------|----------|
| Portrait | 1080x1440 (3:4) | Tall | Social media carousel (swiping) |
| Landscape | 1024x436 (~2.35:1) | Wide | Article covers, blog headers, WeChat |

**Layout must be responsive to both ratios:**
- Avoid absolute vertical positioning that breaks at 436px height
- Use flexbox with `justify-content: center` to center content vertically
- Reduce font sizes for landscape: cover title ~42px (vs 72px portrait), body ~22px (vs 30px)
- Use CSS media queries or `min()` / `clamp()` for fluid sizing
- Safe zone for landscape: Top 30px, Bottom 30px, Left 50px, Right 50px

### Output

```
carousel_output/
├── carousel_001.png            (portrait, 1080x1440)
├── carousel_002.png
├── ...
├── carousel_010.png
├── carousel_cover.png          (portrait thumbnail)
├── cover_1024x436_001.png      (landscape, 1024x436)
├── cover_1024x436_002.png
├── ...
├── cover_1024x436_010.png
└── _post_text.txt              (optional: social media caption)
```

---

## Phase 4: Post Text Generation (Optional)

Generate social media caption for the carousel post.

**Output: _post_text.txt**

```
【标题】5个睡眠秘诀，让你每天精神百倍

【正文】
最近一直在研究睡眠质量的提升方法，试了无数种方式后，总结出这5个最有效的秘诀！
从今天开始改变，你会发现整个人的状态都不一样了~
尤其是第3个方法，真的是相见恨晚！

【标签】
#睡眠质量 #健康生活 #小技巧 #自我提升 #生活方式

【互动引导】
你有什么助眠好方法吗？评论区分享一下吧~
```

**Caption structure:**
1. **Title** -- Attention-grabbing, includes key topic
2. **Body** -- 2-4 sentences, conversational, references the carousel content
3. **Tags** -- 5-8 relevant hashtags
4. **Engagement hook** -- Question or call-to-action for comments

---

## Layout Design Rules

### Safe Zone Enforcement

<HARD-GATE>
All text and critical visual elements MUST stay within the safe zone:
- Top: 120px from top edge
- Bottom: 180px from bottom edge
- Left/Right: 60px from each edge

Decorative elements (background patterns, color blocks) may extend to edges.
Text must NEVER overlap platform UI areas.
</HARD-GATE>

### Visual Rhythm

A good carousel has visual rhythm across pages:

| Technique | How | Example |
|-----------|-----|---------|
| **Consistent header** | Same title area style on all content pages | Title always top-left, same size/color |
| **Page indicator** | Consistent position and style on all pages | Bottom-right, same muted color |
| **Alternating accent** | Alternate accent color usage between pages | Even pages: accent bg, odd pages: accent text |
| **Progressive reveal** | Content builds across pages | Each tip page reveals one more item |
| **Consistent card style** | Same card shape, shadow, border radius | All tip cards have same corner radius |
| **Background continuity** | Same background treatment on all pages | Same gradient, same decorative elements |

### White Space

Social media carousel images need MORE white space than print or web:
- Minimum 40px between content sections
- Minimum 60px padding on sides
- Cover page: 30%+ should be "empty" (background/decoration, not text)
- Content pages: 20%+ breathing room

**Why:** Users scroll fast on mobile. Dense text = skip. Generous spacing = readability.

### Color Usage

| Element | Recommendation |
|---------|---------------|
| Background | 1-2 colors max across all pages |
| Text | 1 color for body, accent for highlights |
| Accent | Used sparingly -- titles, numbers, icons |
| Cards | Slight contrast against background |

**Per-carousel limit:** 3-4 colors total (bg + text + accent + card).

---

## Carousel Content Types & Page Counts

| Content Type | Typical Pages | Cover Style | Content Layout | Ending |
|-------------|--------------|-------------|----------------|--------|
| Tips/How-to | 6-10 | Number list | Tip Card | Summary + CTA + Poster |
| Knowledge/Science | 6-12 | Shock stat | Text-Heavy + Data Card | Summary + Poster |
| Story/Personal | 8-15 | Story teaser | Text-Heavy + Quote Card | Emotional ending + Poster |
| Comparison | 6-8 | Comparison | Split Image | Verdict + Poster |
| Checklist | 6-10 | Number list | Checklist | CTA + Poster |
| Emotional/Quotes | 5-8 | Question | Quote Card | CTA |
| Recipe/DIY | 6-12 | How-to | Step Flow + Tip Card | Final result + Poster |
| Product review | 6-10 | Number/Bold | Tip Card + Data Card | Verdict + CTA + Poster |

---

## Decorative Elements

Unlike video animations, carousel images rely on static decorative elements for visual interest:

### Background Treatments

| Type | CSS | Best For |
|------|-----|----------|
| **Solid + gradient accent** | `background: #FFF8F0;` with positioned gradient div | Lifestyle, warm |
| **Soft gradient** | `background: linear-gradient(135deg, #FFF8F0, #FFE8D6)` | Knowledge, calm |
| **Pattern overlay** | SVG pattern at low opacity | All styles |
| **Color blocks** | Solid color rectangles at edges | Bold, dramatic |
| **Blob shapes** | CSS border-radius shapes with blur | Organic, modern |
| **Geometric lines** | Thin lines, dots, or grid | Clean, corporate |
| **Texture** | Noise or grain overlay | Editorial, premium |

### Decorative SVG Elements

Simple SVG shapes that add visual interest without emoji:
- Wavy dividers between sections
- Circle/dot patterns
- Leaf/branch/flower line art (for lifestyle)
- Geometric shapes (for knowledge/tech)
- Arrow indicators for flow/progress

---

## Rules (Non-Negotiable)

1. **No animation** -- Carousel images are static HTML. No GSAP, no CSS animation, no transitions.
2. **No emoji** -- Use SVG icons or decorative shapes instead.
3. **Safe zone compliance** -- All text within safe margins.
4. **Consistent palette** -- Same colors across all pages in one carousel.
5. **Cover is king** -- Cover page must hook the viewer into swiping.
6. **One point per page** -- Each image delivers one clear message.
7. **Readable text** -- Minimum 24px body, high contrast, no decorative fonts for body.
8. **Page indicator** -- All content pages show current/total page number.
9. **Swipe hint on cover** -- Visual cue to encourage interaction.
10. **Mobile-first design** -- Everything must be readable on a phone screen at arm's length.
11. **No web patterns** -- No navbars, no hover states, no interactive elements. These are images.
12. **Output as images** -- Use html2carousel.py to convert HTML to PNG/JPG. No one views the HTML directly.
13. **Cover thumbnail** -- First image must work as a small thumbnail (the post cover).
14. **Maximum 18 images** for Xiaohongshu, 10 for Instagram. Plan page count within platform limits.
15. **<HARD-GATE> Swipe-forward on every page** -- Every page except the last MUST have a visible swipe-forward element (text or icon). No dead-end pages.
16. **<HARD-GATE> Hook density** -- Carousels with 5+ pages must have: opening hook (P1), mid-escalation hook (40-60%), closing hook (last page).
17. **<HARD-GATE> Three-act structure for 6+ pages** -- Pages organized into 起因(~25%) → 经过(~50%) → 结果(~25%).
18. **<HARD-GATE> Inter-page hook propagation** -- every page (except last) must plant a curiosity gap for the next page via cliffhanger, question, half-result, or preview tease.
19. **<HARD-GATE> Cover withholds the answer** -- the cover must create tension that can only be resolved by swiping. No full reveal on Page 1.
20. **<HARD-GATE> Act 3 pays off Act 1** -- the opening hook's promise must be fulfilled in the result pages.
21. **<HARD-GATE> Dual-size output** -- always generate both portrait carousel (1080x1440) AND landscape cover (1024x436). Same HTML, two render passes, ALL pages in both sizes.
22. **<HARD-GATE> Icon usage** -- every data card, section label, checklist item, and version row MUST include a Remix Icon. No text-only cards.
23. **<HARD-GATE> Poster/Summary page** -- carousels with 8+ pages MUST include a final "all-in-one" poster page that tells the complete story in a single flow-diagram layout (Problem → Diagnosis → Root Cause → Solution → Result). This page has no page indicator.

---

## Do Not

1. Do not add animation or transitions -- these are static images.
2. Do not use interactive web elements (buttons, hover, dropdown) -- they won't work in images.
3. Do not put text outside safe zones -- platform UI will cover it.
4. Do not overload a page with text -- max ~100 Chinese characters per page.
5. Do not use more than 4 colors in one carousel.
6. Do not use gradient text or effects that reduce readability.
7. Do not use fonts smaller than 18px -- they won't be readable on mobile.
8. Do not generate images wider than 1080px without explicit user request.
9. Do not forget the page indicator on content pages.
10. Do not make the cover boring -- it's the difference between a swipe and a scroll-past.
11. Do not mix too many layout types -- stick to 2-3 layouts per carousel.
12. Do not use the same layout for every page -- vary rhythm to maintain interest.
13. Do not create a flat middle section -- every 5+ page carousel must have a mid-escalation hook.
14. Do not let any page be a dead end -- every page (except last) needs swipe-forward motivation.
15. Do not reveal the answer on the cover -- withhold the payoff to encourage swiping.
16. Do not use the same hook type on every page -- vary STAT/COUNTER/MYSTERY/CHALLENGE/RESULT/PROMISE.
17. Do not make all pages the same hook strength -- W-shape, not flat line.
18. Do not end a carousel without a closing hook -- PROMISE (follow/like) or MYSTERY (unresolved tease).
19. Do not forget Act 3 must pay off Act 1's hook -- if you asked a question, answer it in the result pages.
20. Do not use banned swipe-forward phrases: "接下来看", "下面介绍", "然后是" -- use curiosity gaps instead.
21. Do not use text-only data cards -- every card must have an icon badge.
22. Do not hardcode font sizes in px -- use CSS custom properties (`var(--fs-body)`, etc.) for responsive dual-size rendering.
23. Do not skip the poster page for carousels with 8+ pages.
24. Do not use separate HTML files for portrait and landscape -- same HTML, two render passes via `@media (max-height: 600px)`.

---

## Icon Usage Rules

<HARD-GATE>
Every carousel MUST use Remix Icons throughout. Text-only cards are banned.
</HARD-GATE>

### Icon Placement Requirements

| Element | Icon Required | Example Icons |
|---------|--------------|---------------|
| Section labels | Icon before text | `ri-alarm-warning-line`, `ri-search-eye-line`, `ri-tools-line` |
| Data cards | Icon badge next to value | `ri-fire-line`, `ri-trophy-line`, `ri-arrow-up-line` |
| Checklist items | Icon in check circle | `ri-check-line` (done), `ri-scissors-cut-line`, `ri-settings-4-line` |
| Split labels | Icon after label text | `ri-bug-line` (bad side), `ri-shield-star-line` (good side) |
| Version rows | Icon in avatar circle | `ri-bug-line` (bad), `ri-rocket-2-line` (fixed), `ri-trophy-line` (best) |
| Summary points | Icon before number | `ri-fire-line`, `ri-infinity-line`, `ri-layout-grid-line` |
| Callout boxes | Icon before text | `ri-lightbulb-line`, `ri-code-s-slash-line`, `ri-rocket-line` |

### Icon Badge Pattern

Every data card and list item should use an icon badge:

```html
<div class="icon-badge accent"><i class="ri-trophy-line"></i></div>
```

```css
.icon-badge {
  display: inline-flex; align-items: center; justify-content: center;
  width: 48px; height: 48px; border-radius: 14px;
  font-size: 26px; flex-shrink: 0;
}
.icon-badge.accent { background: var(--surface); color: var(--accent); }
.icon-badge.danger { background: rgba(231,76,60,0.08); color: var(--danger); }
.icon-badge.success { background: rgba(0,184,148,0.08); color: var(--success); }

@media (max-height: 600px) {
  .icon-badge { width: 24px; height: 24px; font-size: 13px; border-radius: 6px; }
}
```

### Recommended Icons by Context

| Context | Remix Icons |
|---------|------------|
| Problem / danger | `ri-alarm-warning-line`, `ri-fire-line`, `ri-bug-line`, `ri-close-circle-line`, `ri-error-warning-line`, `ri-skull-line` |
| Diagnosis / search | `ri-search-eye-line`, `ri-focus-3-line`, `ri-speed-line`, `ri-arrow-up-circle-line` |
| Comparison | `ri-git-merge-line`, `ri-contrast-line`, `ri-arrow-left-right-line` |
| Solution / fix | `ri-tools-line`, `ri-scissors-cut-line`, `ri-settings-4-line`, `ri-combine-line` |
| Success / result | `ri-trophy-line`, `ri-shield-check-line`, `ri-shield-star-line`, `ri-arrow-down-line`, `ri-checkbox-circle-line` |
| Data / stats | `ri-bar-chart-grouped-line`, `ri-line-chart-line`, `ri-percent-line` |
| Training | `ri-settings-4-line`, `ri-heart-pulse-line` |
| Extrapolation | `ri-rocket-line`, `ri-infinity-line`, `ri-rocket-2-line` |
| Overview / poster | `ri-file-list-3-line`, `ri-layout-grid-line`, `ri-dashboard-line` |
| CPU / model | `ri-cpu-line`, `ri-brain-line` |

---

## Responsive CSS for Dual-Size (Portrait + Landscape)

All carousel HTML MUST work at both 1080x1440 and 1024x436 using CSS custom properties and `@media (max-height: 600px)`.

### Responsive Variable Pattern

```css
:root {
  /* Portrait defaults (1080x1440) */
  --safe-top: 120px;
  --safe-bottom: 180px;
  --safe-side: 60px;
  --fs-hero: 180px;
  --fs-cover-title: 72px;
  --fs-cover-sub: 36px;
  --fs-page-title: 48px;
  --fs-body: 30px;
  --fs-label: 24px;
  --fs-caption: 20px;
  --fs-section: 18px;
  --fs-data-lg: 44px;
  --fs-data-md: 38px;
  --fs-data-sm: 34px;
  --radius-card: 16px;
  --gap-card: 16px;
  --pad-card: 24px 28px;
}

@media (max-height: 600px) {
  :root {
    /* Landscape overrides (1024x436) */
    --safe-top: 24px;
    --safe-bottom: 24px;
    --safe-side: 40px;
    --fs-hero: 56px;
    --fs-cover-title: 36px;
    --fs-cover-sub: 16px;
    --fs-page-title: 26px;
    --fs-body: 16px;
    --fs-label: 14px;
    --fs-caption: 12px;
    --fs-section: 11px;
    --fs-data-lg: 28px;
    --fs-data-md: 22px;
    --fs-data-sm: 20px;
    --radius-card: 10px;
    --gap-card: 8px;
    --pad-card: 10px 14px;
  }
  .carousel { width: 1024px; }
  .slide { width: 1024px; height: 436px; }
}
```

### Usage in Components

All font sizes, padding, gaps, and radii use `var()` references:

```css
.page-title { font-size: var(--fs-page-title); }
.data-value { font-size: var(--fs-data-lg); }
.data-card { padding: var(--pad-card); border-radius: var(--radius-card); }
.data-grid { gap: var(--gap-card); }
.content { top: var(--safe-top); left: var(--safe-side); right: var(--safe-side); bottom: var(--safe-bottom); }
```

### Cover Layout Switch

The cover page switches from vertical (portrait) to horizontal (landscape):

```css
.cover-content {
  /* portrait: centered vertical stack */
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

@media (max-height: 600px) {
  .cover-content {
    /* landscape: horizontal split */
    flex-direction: row !important;
    gap: 24px !important;
  }
  .cover-left { text-align: left !important; flex: 1; }
  .cover-right { flex-shrink: 0; }
}
```

---

## Poster / All-In-One Page

<HARD-GATE>
Carousels with 8+ pages MUST include a final poster page that condenses the entire story into one dark-themed infographic.
The poster page uses a DIFFERENT visual style from the rest of the carousel: dark background, glowing nodes, grid overlay.
</HARD-GATE>

### Layout: Dark Theme Two-Column Flow

```
┌─────────────────────────────────────────────────┐
│  Dark background (#0D1117) + grid overlay        │
│  + gradient blobs (blue + green glow)            │
│                                                  │
│          [POSTER BADGE]                           │
│       AI模型外推崩溃                              │
│    从根因定位到完美修复 → 全链路分析               │
│                                                  │
│  ┌── LEFT COLUMN ──┐ │ ┌── RIGHT COLUMN ──┐     │
│  │ [!] 问题         │ │ │ [🔧] 修复        │     │
│  │ PPL 5.9→33286   │ │ │ Loss +0.8%       │     │
│  │  [5625x]         │ │ │ PPL -4.2%        │     │
│  │    ↓             │ │ │    ↓             │     │
│  │ [🔍] 诊断        │ │ │ [🏆] 结果        │     │
│  │ L8: 871→11914   │ │ │ 128K stable      │     │
│  │  [13.7x]         │ │ │ [chips][chips]   │     │
│  │    ↓             │ │ │    ↓             │     │
│  │ [🔀] 根因        │ │ │ [🧠] CTA         │     │
│  │ cummax 512 vs    │ │ │ 关注获取更多      │     │
│  │ 8x80             │ │ │                  │     │
│  └──────────────────┘ │ └──────────────────┘     │
│              vertical divider line                │
└─────────────────────────────────────────────────┘
```

### Visual Design

| Property | Value |
|----------|-------|
| Background | `#0D1117` (dark) with grid overlay + gradient blobs |
| Text | `#E6EDF3` (light) / `#8B949E` (muted) |
| Danger | `#F87171` with `rgba(231,76,60,0.15)` backgrounds |
| Success | `#34D399` with `rgba(0,184,148,0.15)` backgrounds |
| Accent | `#74B9FF` with `rgba(9,132,227,0.15)` backgrounds |
| Nodes | Semi-transparent cards with subtle borders |
| Connectors | Thin vertical lines + arrow icons |
| Divider | Vertical gradient line between columns |

### CSS Pattern

```css
.poster-page { background: #0D1117; color: #E6EDF3; }
.poster-bg-grad {
  background: radial-gradient(ellipse at 20% 20%, rgba(9,132,227,0.15) 0%, transparent 50%),
              radial-gradient(ellipse at 80% 80%, rgba(0,184,148,0.1) 0%, transparent 50%),
              linear-gradient(180deg, #0D1117 0%, #161B22 100%);
}
.poster-bg-grid {
  background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 48px 48px;
}
.poster-node {
  padding: 14px 16px; background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.06); border-radius: 14px;
}
.poster-node.danger-node {
  border-color: rgba(231,76,60,0.2); background: rgba(231,76,60,0.06);
}
.poster-node.result-node {
  border-color: rgba(0,184,148,0.25); background: rgba(0,184,148,0.06);
  box-shadow: 0 0 24px rgba(0,184,148,0.08);
}
```

### Poster Page Rules

1. **No page indicator** -- poster is standalone, no N/M numbering
2. **No swipe-forward** -- poster is always the last page
3. **Two-column layout**: Left = Problem/Diagnosis/Cause, Right = Solution/Result/CTA
4. **Dark theme** -- completely different from light carousel pages
5. **Glowing nodes** -- danger (red), accent (blue), success (green) with semi-transparent backgrounds
6. **Vertical connectors** between nodes with arrow icons
7. **Result node highlighted** -- green glow shadow + colored border
8. **Result chips** -- colored tags showing each model variant's PPL
9. **Footer CTA** -- gradient icon circle + follow text
10. **Responsive**: compresses to fit 436px height with scaled-down nodes

---

## Quality Checklist

### Cover Page (Hook Cover -- Must ALL pass)

- [ ] **Hook title creates curiosity** (uses one of 10 hook patterns, NOT "XXX分享")
- [ ] **Visual punch element present** (oversized number, bold color, dramatic contrast)
- [ ] **No page indicator on cover**
- [ ] **Swipe hint present** (arrow, dots, or visual cue)
- [ ] **Readable as a small thumbnail** (60x80px or smaller)
- [ ] **Text within safe zones**
- [ ] **Cover withholds the answer** (viewer must swipe to resolve)
- [ ] **Hook strength = 5** (this is the strongest or tied-strongest page)

### Hook System (Carousels with 5+ pages -- Must ALL pass)

- [ ] **Opening hook present** (Page 1 satisfies cover hook rules)
- [ ] **Mid-escalation hook present** (40-60% range has STAT/COUNTER/MYSTERY/CHALLENGE)
- [ ] **Closing hook present** (last page ends with PROMISE or MYSTERY)
- [ ] **Hook propagation chain intact** (every page except last has swipe-forward element)
- [ ] **No dead-end pages** (no page that gives no reason to keep swiping)
- [ ] **Half-result hooks present** (at least 1 page resolves A but opens B)
- [ ] **Hook strength follows W-shape** (not flat, not all max, varied)
- [ ] **At least 3 different hook types** used across the carousel
- [ ] **Three-act structure followed** (起因/经过/结果 with correct proportions)
- [ ] **Act 3 pays off Act 1** (opening hook answered in result pages)

### Content Pages

- [ ] One clear point per page
- [ ] Page indicator shows current/total
- [ ] Text within safe zones
- [ ] Readable at mobile viewing distance
- [ ] Consistent visual style with other pages
- [ ] Adequate white space (20%+ breathing room)
- [ ] Swipe-forward element present (except last page)
- [ ] Icon badges on all data cards and list items

### Dual-Size Rendering

- [ ] HTML uses CSS custom properties for all sizes
- [ ] `@media (max-height: 600px)` overrides present for landscape
- [ ] Cover layout switches to horizontal in landscape
- [ ] Icon badges scale down in landscape (24px)
- [ ] Both sizes generated: portrait prefix `carousel_` + landscape prefix `cover_1024x436_`
- [ ] Both sizes output ALL pages (same count)

### Poster Page (Carousels with 8+ pages)

- [ ] Final page is a flow-diagram poster (Problem → Diagnosis → Root Cause → Solution → Result)
- [ ] Each step has icon badge, title, one-line description, key data
- [ ] Final result step has accent border highlight
- [ ] Version comparison chips present with colored tags
- [ ] No page indicator on poster page
- [ ] No swipe-forward on poster page

### Overall Carousel

- [ ] Consistent palette across all pages
- [ ] Consistent typography (max 2 fonts)
- [ ] Visual rhythm maintained (not monotonous)
- [ ] Content flows logically (hook -> context -> content -> conclusion)
- [ ] Page count within platform limits
- [ ] Cover thumbnail works as post cover
- [ ] Post caption generated with hashtags and engagement hook

---

## Real-World Example

**User input:** "帮我做一个小红书图文，讲5个提高睡眠质量的方法"

**Execution:**

### Step 1: Carousel Hook Storyboard (CT1)

| Page | Act | Title | Hook Type | Swipe Forward | Strength |
|------|-----|-------|-----------|---------------|----------|
| 1 | 起因 | "5个睡眠秘诀" | STAT | "为什么你总是睡不好？→" | 5 |
| 2 | 起因 | "为什么睡不好？" | CHALLENGE | "第1个秘诀就够颠覆了 →" | 3 |
| 3 | 经过 | "秘诀1: 固定作息" | -- | "第2个秘诀更反直觉 →" | 2 |
| 4 | 经过 | "秘诀2: 远离手机" | COUNTER | "解决了入睡——但深度睡眠呢？→" | 4 |
| 5 | 经过 | "秘诀3: 室温20度" | -- | "还有2个，第4个最关键 →" | 2 |
| 6 | 经过 | "秘诀4: 晚餐别太饱" | -- | "最后一个才是终极武器 →" | 3 |
| 7 | 结果 | "秘诀5: 睡前冥想" | RESULT | "这就是完整方案，今晚开始！" | 5 |
| 8 | 结果 | "今晚开始试试" | PROMISE | "关注我，下期讲晨间习惯" | 3 |

**Hook strength curve:** 5 → 3 → 2 → 4 → 2 → 3 → 5 → 3 (W-shape)
**Hook propagation chain:** Every page has swipe-forward. No dead ends.
**Three-act:** P1-2 起因(25%) → P3-6 经过(50%) → P7-8 结果(25%)

### Step 2: Generate HTML with warm-lifestyle palette

- Background: warm cream #FFF8F0
- Text: dark brown #2D2016
- Accent: warm orange #E8833A
- Cover: oversized "5" in accent color, hook title "5个睡眠秘诀", subtitle "让你每天精神百倍"
- Every content page has swipe-forward element at bottom (accent color, arrow icon)
- Page 4 (mid-hook) uses COUNTER layout with contrasting card style

### Step 3: Run script (dual-size output)

```bash
# Run 1: Portrait (1080x1440, all pages)
python scripts/html2carousel.py sleep_tips.html -o sleep_output/ --caption

# Run 2: Landscape (1024x436, all pages)
python scripts/html2carousel.py sleep_tips.html -o sleep_output/ --width 1024 --height 436 --prefix cover_1024x436
```

### Step 4: Output

```
sleep_output/
├── carousel_001.png ~ carousel_008.png   (portrait, 1080x1440)
├── carousel_cover.png                     (portrait thumbnail)
├── cover_1024x436_001.png ~ _008.png      (landscape, 1024x436)
└── _post_text.txt                         (social media caption)
```

---

## References (Loaded on Demand)

| File | Read When |
|------|-----------|
| `visual-styles.md` | Selecting visual style for carousel |
| `house-style.md` | Generating HTML without user-specified style |
| `references/carousel-patterns.md` | Choosing layout templates for each page |
| `references/typography.md` | Font selection, text sizing, pairing |

### Palettes

| File | Best For |
|------|----------|
| `palettes/warm-lifestyle.md` | Lifestyle, food, wellness, home |
| `palettes/pastel-soft.md` | Beauty, fashion, baby, gentle topics |
| `palettes/bold-social.md` | Fitness, motivation, bold statements |
| `palettes/clean-knowledge.md` | Education, science, tech tips |
| `palettes/dark-aesthetic.md` | Luxury, mood, night, premium |
| `palettes/nature-fresh.md` | Outdoors, sustainability, health |
| `palettes/minimal-mono.md` | Quotes, typography, editorial |

---

## Parameter Quick Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| Input HTML | (required) | Carousel HTML file |
| Output dir | `./carousel_output/` | Output PNG directory |
| Width | 1080 | Image width in pixels |
| Height | 1440 | Image height in pixels |
| Slide selector | `.slide` | CSS selector for slide elements |
| Format | `png` | Output format (png/jpg) |
| Quality | 95 | JPG quality |
| Prefix | `carousel` | Output filename prefix |
| Caption | `--caption` | Generate post caption text |
| Platform | `--platform` | Target platform (xiaohongshu/instagram/general) |
