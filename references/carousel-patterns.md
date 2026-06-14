# Carousel Layout Patterns

Ready-to-use layout templates for each carousel page type.
Each pattern includes HTML structure, CSS styles, and usage notes.

---

## Pattern 1: Cover Card (Page 1 Hook)

The first page of every carousel. Must hook the viewer.

```html
<div class="slide cover">
  <div class="cover-bg">
    <div class="cover-accent-block"></div>
    <div class="cover-decoration"></div>
  </div>
  <div class="content">
    <div class="cover-number">5</div>
    <h1 class="cover-title">个睡眠秘诀</h1>
    <p class="cover-subtitle">让你每天精神百倍</p>
    <div class="swipe-hint">
      <span class="swipe-arrow">></span>
      <span class="swipe-text">左滑查看</span>
    </div>
  </div>
</div>
```

```css
.cover {
  background: var(--bg);
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}
.cover-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
}
.cover-accent-block {
  position: absolute;
  top: -80px;
  right: -80px;
  width: 400px;
  height: 400px;
  background: var(--accent);
  border-radius: 50%;
  opacity: 0.12;
}
.cover-decoration {
  position: absolute;
  bottom: 200px;
  left: -40px;
  width: 200px;
  height: 6px;
  background: var(--accent);
  opacity: 0.3;
  border-radius: 3px;
}
.cover-number {
  font-size: 160px;
  font-weight: 900;
  color: var(--accent);
  line-height: 0.9;
  margin-bottom: -20px;
}
.cover-title {
  font-size: 80px;
  font-weight: 800;
  color: var(--fg);
  line-height: 1.1;
  margin: 0;
}
.cover-subtitle {
  font-size: 36px;
  font-weight: 400;
  color: var(--muted);
  margin-top: 16px;
}
.swipe-hint {
  position: absolute;
  bottom: 80px;
  right: 60px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--muted);
  font-size: 18px;
}
.swipe-arrow {
  font-size: 24px;
  color: var(--accent);
}
```

---

## Pattern 2: Tip Card

For list items, numbered tips, steps.

```html
<div class="slide tip-page">
  <div class="content">
    <div class="page-header">
      <span class="tip-number">01</span>
      <h2 class="page-title">固定作息时间</h2>
    </div>
    <div class="tip-card">
      <div class="tip-icon">
        <i class="ri-time-line"></i>
      </div>
      <p class="tip-body">
        每天同一时间入睡和起床，即使周末也不例外。
        你的生物钟会感谢你。
      </p>
    </div>
    <div class="tip-highlight">
      <span class="highlight-label">关键</span>
      <span class="highlight-text">坚持21天养成习惯</span>
    </div>
  </div>
  <div class="page-indicator">
    <span class="current">3</span>/<span class="total">8</span>
  </div>
</div>
```

```css
.tip-page { background: var(--bg); }
.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 32px;
}
.tip-number {
  font-size: 64px;
  font-weight: 900;
  color: var(--accent);
  line-height: 1;
}
.page-title {
  font-size: 48px;
  font-weight: 700;
  color: var(--fg);
  margin: 0;
}
.tip-card {
  background: var(--card);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.06);
}
.tip-icon {
  font-size: 48px;
  color: var(--accent);
  margin-bottom: 20px;
}
.tip-body {
  font-size: 30px;
  color: var(--fg);
  line-height: 1.7;
  margin: 0;
}
.tip-highlight {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 28px;
  padding: 16px 24px;
  background: var(--surface);
  border-radius: 12px;
}
.highlight-label {
  font-size: 20px;
  font-weight: 700;
  color: var(--accent);
  text-transform: uppercase;
}
.highlight-text {
  font-size: 24px;
  color: var(--fg);
}
.page-indicator {
  position: absolute;
  bottom: 60px;
  right: 60px;
  font-size: 18px;
  color: var(--muted);
}
.page-indicator .current {
  color: var(--accent);
  font-weight: 700;
}
```

---

## Pattern 3: Text-Heavy

For explanations, paragraphs, story beats.

```html
<div class="slide text-page">
  <div class="content">
    <h2 class="page-title">为什么睡不好？</h2>
    <div class="text-divider"></div>
    <p class="text-body">
      80%的睡眠问题来自日常坏习惯。睡前刷手机、
      晚餐吃太饱、卧室温度太高......
      这些看似小事，却在偷偷破坏你的睡眠质量。
    </p>
    <div class="text-callout">
      <i class="ri-lightbulb-line"></i>
      <span>了解原因是改变的第一步</span>
    </div>
  </div>
  <div class="page-indicator">
    <span class="current">2</span>/<span class="total">8</span>
  </div>
</div>
```

```css
.text-page { background: var(--bg); }
.text-divider {
  width: 60px;
  height: 4px;
  background: var(--accent);
  border-radius: 2px;
  margin: 24px 0 32px;
}
.text-body {
  font-size: 32px;
  color: var(--fg);
  line-height: 1.8;
  margin: 0;
}
.text-callout {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 40px;
  padding: 20px 28px;
  background: var(--surface);
  border-left: 4px solid var(--accent);
  border-radius: 0 12px 12px 0;
  font-size: 24px;
  color: var(--muted);
}
```

---

## Pattern 4: Quote Card

For key statements, emotional moments, important takeaways.

```html
<div class="slide quote-page">
  <div class="content" style="justify-content: center; text-align: center;">
    <div class="quote-mark">"</div>
    <blockquote class="quote-text">
      好的睡眠不是奢侈品，而是你应得的基本权利。
    </blockquote>
    <div class="quote-divider"></div>
    <p class="quote-author">睡眠专家 Dr. Walker</p>
  </div>
  <div class="page-indicator">
    <span class="current">5</span>/<span class="total">8</span>
  </div>
</div>
```

```css
.quote-page { background: var(--bg); }
.quote-mark {
  font-size: 120px;
  line-height: 0.5;
  color: var(--accent);
  opacity: 0.3;
  font-family: Georgia, serif;
}
.quote-text {
  font-size: 40px;
  font-weight: 300;
  color: var(--fg);
  line-height: 1.6;
  max-width: 800px;
  margin: 20px auto 0;
  font-style: italic;
}
.quote-divider {
  width: 40px;
  height: 2px;
  background: var(--accent);
  margin: 28px auto;
}
.quote-author {
  font-size: 22px;
  color: var(--muted);
}
```

---

## Pattern 5: Checklist

For to-do lists, habits, feature lists.

```html
<div class="slide checklist-page">
  <div class="content">
    <h2 class="page-title">睡前检查清单</h2>
    <div class="checklist">
      <div class="check-item">
        <div class="check-box done"><i class="ri-check-line"></i></div>
        <span class="check-text">手机放到卧室外</span>
      </div>
      <div class="check-item">
        <div class="check-box done"><i class="ri-check-line"></i></div>
        <span class="check-text">卧室温度调到20度</span>
      </div>
      <div class="check-item">
        <div class="check-box"><i class="ri-check-line"></i></div>
        <span class="check-text">做5分钟冥想</span>
      </div>
      <div class="check-item">
        <div class="check-box"><i class="ri-check-line"></i></div>
        <span class="check-text">关灯，拉好窗帘</span>
      </div>
    </div>
  </div>
  <div class="page-indicator">
    <span class="current">6</span>/<span class="total">8</span>
  </div>
</div>
```

```css
.checklist-page { background: var(--bg); }
.checklist {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 32px;
}
.check-item {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px 28px;
  background: var(--card);
  border-radius: 16px;
}
.check-box {
  width: 40px;
  height: 40px;
  border: 2px solid var(--muted);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: transparent;
  font-size: 24px;
  flex-shrink: 0;
}
.check-box.done {
  background: var(--accent);
  border-color: var(--accent);
  color: white;
}
.check-text {
  font-size: 28px;
  color: var(--fg);
}
.check-item:has(.done) .check-text {
  color: var(--muted);
  text-decoration: line-through;
}
```

---

## Pattern 6: Summary / CTA (Last Page)

For closing page with key takeaway and call-to-action.

```html
<div class="slide summary-page">
  <div class="content" style="justify-content: center; text-align: center;">
    <div class="summary-badge">总结</div>
    <h2 class="summary-title">今晚就开始试试</h2>
    <p class="summary-body">
      从5个秘诀中选一个开始，坚持21天，你会发现改变。
    </p>
    <div class="cta-box">
      <div class="cta-icon"><i class="ri-heart-line"></i></div>
      <p class="cta-text">觉得有用就收藏起来吧~</p>
      <p class="cta-sub">关注我，每天分享实用小技巧</p>
    </div>
  </div>
</div>
```

```css
.summary-page { background: var(--bg); }
.summary-badge {
  display: inline-block;
  padding: 8px 24px;
  background: var(--accent);
  color: white;
  border-radius: 20px;
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 24px;
}
.summary-title {
  font-size: 56px;
  font-weight: 800;
  color: var(--fg);
  margin: 0 0 20px;
}
.summary-body {
  font-size: 28px;
  color: var(--muted);
  line-height: 1.6;
  margin: 0 0 40px;
}
.cta-box {
  background: var(--card);
  border-radius: 20px;
  padding: 32px;
  text-align: center;
}
.cta-icon {
  font-size: 40px;
  color: var(--accent);
  margin-bottom: 12px;
}
.cta-text {
  font-size: 28px;
  color: var(--fg);
  font-weight: 600;
  margin: 0 0 8px;
}
.cta-sub {
  font-size: 22px;
  color: var(--muted);
  margin: 0;
}
```

---

## Pattern 7: Data Card

For statistics, comparisons, big numbers.

```html
<div class="slide data-page">
  <div class="content">
    <h2 class="page-title">睡眠数据</h2>
    <div class="data-grid">
      <div class="data-card">
        <div class="data-value">80%</div>
        <div class="data-label">的睡眠问题来自坏习惯</div>
      </div>
      <div class="data-card">
        <div class="data-value">7-9h</div>
        <div class="data-label">成年人推荐睡眠时长</div>
      </div>
      <div class="data-card">
        <div class="data-value">21天</div>
        <div class="data-label">养成一个新习惯的时间</div>
      </div>
    </div>
  </div>
  <div class="page-indicator">
    <span class="current">4</span>/<span class="total">8</span>
  </div>
</div>
```

```css
.data-page { background: var(--bg); }
.data-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 32px;
}
.data-card {
  background: var(--card);
  border-radius: 16px;
  padding: 28px 32px;
  border-left: 4px solid var(--accent);
}
.data-value {
  font-size: 52px;
  font-weight: 900;
  color: var(--accent);
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
}
.data-label {
  font-size: 24px;
  color: var(--muted);
  margin-top: 8px;
}
```

---

## Pattern 8: Split Layout

For before/after, comparison, two-column content.

```html
<div class="slide split-page">
  <div class="content">
    <h2 class="page-title">改变前后</h2>
    <div class="split-container">
      <div class="split-left">
        <div class="split-label">Before</div>
        <div class="split-item">晚上12点还在刷手机</div>
        <div class="split-item">翻来覆去睡不着</div>
        <div class="split-item">早上起不来</div>
      </div>
      <div class="split-divider">VS</div>
      <div class="split-right">
        <div class="split-label">After</div>
        <div class="split-item">10点半准时关灯</div>
        <div class="split-item">沾枕头就睡着</div>
        <div class="split-item">自然醒，精神满满</div>
      </div>
    </div>
  </div>
  <div class="page-indicator">
    <span class="current">7</span>/<span class="total">8</span>
  </div>
</div>
```

```css
.split-page { background: var(--bg); }
.split-container {
  display: flex;
  gap: 0;
  margin-top: 32px;
  flex: 1;
}
.split-left, .split-right {
  flex: 1;
  padding: 28px;
  border-radius: 16px;
}
.split-left { background: rgba(220, 38, 38, 0.06); }
.split-right { background: rgba(34, 197, 94, 0.06); }
.split-label {
  font-size: 20px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 20px;
}
.split-left .split-label { color: #DC2626; }
.split-right .split-label { color: #22C55E; }
.split-divider {
  display: flex;
  align-items: center;
  padding: 0 16px;
  font-size: 28px;
  font-weight: 900;
  color: var(--muted);
}
.split-item {
  font-size: 26px;
  color: var(--fg);
  padding: 8px 0;
  line-height: 1.5;
}
```

---

## Pattern Selection Guide

| Content Type | Page Position | Pattern | Notes |
|-------------|--------------|---------|-------|
| Numbered list | Page 1 | Cover Card | Oversized number hero |
| Introduction | Page 2 | Text-Heavy | Set the stage |
| Tips / steps | Pages 3-N | Tip Card | One tip per page |
| Key statement | Any | Quote Card | Break the rhythm |
| Data / stats | Any | Data Card | Big numbers |
| Checklist | Any | Checklist | Actionable items |
| Comparison | Any | Split Layout | Side by side |
| Summary | Last page | Summary/CTA | Close with action |

---

## Swipe-Forward Element (Required on All Non-Last Pages)

Every content page (except the final page) MUST include a swipe-forward hook element. This is the carousel equivalent of the inter-page hook propagation chain.

### HTML

```html
<div class="swipe-forward">
  <span class="swipe-text">下一个秘诀更颠覆</span>
  <i class="ri-arrow-right-s-line"></i>
</div>
```

### CSS

```css
.swipe-forward {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  margin-top: auto;
  padding-top: 20px;
  font-size: 22px;
  color: var(--accent);
  font-weight: 500;
}
.swipe-forward i {
  font-size: 26px;
}
```

### Position

Inside `.content`, at the bottom, right-aligned. Uses `margin-top: auto` to push to bottom of flex container.

### Swipe-Forward Text Patterns

Use the `swipe_forward` field from `_carousel_design.json`. Patterns:

| Pattern | Example Text | Hook Type |
|---------|-------------|-----------|
| **Cliffhanger** | "...但这还不是最离谱的" | MYSTERY |
| **Question bridge** | "你知道哪个习惯最伤睡眠吗？" | CHALLENGE |
| **Ranking tease** | "第4个才是真正的game changer" | PROMISE |
| **Half-result** | "解决了入睡——但怎么保证深度睡眠？" | COUNTER |
| **Contrast setup** | "这是改变前...下一页是改变后" | RESULT |
| **Number tease** | "还有3个秘诀，记得滑到最后" | PROMISE |
| **Simple cue** | "左滑查看 →" | (minimal, use only if page content is already strong) |

### BANNED Swipe-Forward Patterns

- "接下来看..." / "下面介绍..." / "然后是..." (boring, no tension)
- "左滑" alone without any curiosity text (lazy)
- Same text on every page (mechanical, feels like spam)
- No swipe-forward at all (dead end = user closes carousel)

---

## Hook-Aware Pattern Selection

When selecting patterns, consider the page's hook role:

| Hook Role | Pattern | Swipe-Forward Strategy |
|-----------|---------|----------------------|
| **Opening** (P1) | Cover Card | Swipe hint arrow + hook subtitle |
| **Problem framing** (P2) | Text-Heavy | "But here's what nobody tells you →" |
| **Development** (P3-N) | Tip Card | Ranking tease / preview |
| **Mid-escalation** (40-60%) | Tip Card with contrasting style | Half-result hook |
| **Payoff** (N-1) | Tip Card or Data Card | "And the last one is the ultimate →" |
| **Closing** (N) | Summary/CTA | PROMISE hook ("关注我，下期更精彩") |
| **Pattern break** | Quote Card (inserted among Tip Cards) | Restores attention with contrast |
| **Version comparison** | Version Card grid | Comparing multiple model/product variants |
| **Poster / all-in-one** | Flow Diagram (final page) | Problem → Diagnosis → Root Cause → Solution → Result |

---

## Pattern 9: Version Comparison

For comparing multiple model/product variants in a single page. Each row = one variant.

```html
<div class="version-grid">
  <div class="ver-card">
    <div class="ver-icon bad"><i class="ri-bug-line"></i></div>
    <div class="ver-info">
      <div class="ver-name">Model A Baseline</div>
      <div class="ver-desc"><i class="ri-cpu-line" style="margin-right:3px;"></i>No fix applied</div>
    </div>
    <div class="ver-ppl bad">33286</div>
  </div>
  <div class="ver-card">
    <div class="ver-icon ok"><i class="ri-rocket-2-line"></i></div>
    <div class="ver-info">
      <div class="ver-name">Model A + Cap</div>
      <div class="ver-desc"><i class="ri-scissors-cut-line" style="margin-right:3px;"></i>State norm cap applied</div>
    </div>
    <div class="ver-ppl ok">14.7</div>
  </div>
  <div class="ver-card winner">
    <div class="ver-icon best"><i class="ri-trophy-line"></i></div>
    <div class="ver-info">
      <div class="ver-name">Model B + Norm-200</div>
      <div class="ver-desc"><i class="ri-scissors-cut-line" style="margin-right:3px;"></i>State norm cap applied</div>
    </div>
    <div class="ver-ppl best">11.3</div>
  </div>
</div>
```

```css
.version-grid {
  display: flex; flex-direction: column; gap: var(--gap-card);
  margin-top: 20px; flex: 1;
}
.ver-card {
  display: flex; align-items: center; gap: 16px;
  padding: var(--pad-card); background: var(--card);
  border-radius: var(--radius-card); box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.ver-icon {
  width: 44px; height: 44px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px; flex-shrink: 0;
}
.ver-icon.bad { background: rgba(231,76,60,0.08); color: #E74C3C; }
.ver-icon.ok { background: rgba(0,184,148,0.08); color: #00B894; }
.ver-icon.best { background: var(--surface); color: var(--accent); }
.ver-info { flex: 1; }
.ver-name { font-size: var(--fs-label); font-weight: 700; color: var(--fg); }
.ver-desc { font-size: var(--fs-caption); color: var(--muted); margin-top: 2px; }
.ver-ppl { font-size: var(--fs-data-sm); font-weight: 900; flex-shrink: 0; text-align: right; }
.ver-ppl.bad { color: #E74C3C; }
.ver-ppl.ok { color: #00B894; }
.ver-ppl.best { color: var(--accent); }
.ver-card.winner {
  border: 2px solid var(--accent);
  box-shadow: 0 4px 16px rgba(9,132,227,0.12);
}
@media (max-height: 600px) {
  .ver-icon { width: 24px !important; height: 24px !important; font-size: 13px !important; }
  .ver-card { padding: 6px 10px !important; gap: 8px !important; }
}
```

---

## Pattern 10: Poster / All-In-One (Dark Theme Infographic)

The final page of carousels with 8+ pages. A dark-themed, poster-grade infographic that condenses the entire story into a two-column flow.

### HTML

```html
<div class="slide poster-page">
  <div class="poster-bg">
    <div class="poster-bg-grad"></div>
    <div class="poster-bg-grid"></div>
    <div class="poster-bg-circle1"></div>
    <div class="poster-bg-circle2"></div>
  </div>
  <div class="content" style="top:40px;bottom:40px;left:48px;right:48px;">
    <div class="poster-head">
      <div class="poster-badge"><i class="ri-dashboard-3-line" style="margin-right:6px;"></i>POSTER</div>
      <div class="poster-hero-title">AI模型外推崩溃</div>
      <div class="poster-hero-sub">从根因定位到完美修复 → 全链路分析</div>
    </div>
    <div class="poster-body">
      <div class="poster-col">
        <!-- Left: Problem → Diagnosis → Root Cause -->
        <div class="poster-node danger-node">
          <div class="node-dot"><i class="ri-alarm-warning-line"></i></div>
          <div class="node-content">
            <div class="node-title">问题 <i class="ri-fire-line"></i></div>
            <div class="node-text">Description</div>
            <div class="node-stat"><span class="stat-danger">DATA</span> <span class="stat-tag danger-tag">TAG</span></div>
          </div>
        </div>
        <div class="node-connector">...</div>
        <!-- more nodes -->
      </div>
      <div class="poster-divider-v"><div class="divider-v-line"></div></div>
      <div class="poster-col">
        <!-- Right: Solution → Result → CTA -->
        <div class="poster-node">
          <div class="node-dot success"><i class="ri-tools-line"></i></div>
          <div class="node-content">
            <div class="node-title">修复</div>
            <div class="node-text">Description</div>
            <div class="node-stat">DATA</div>
          </div>
        </div>
        <div class="node-connector">...</div>
        <div class="poster-node result-node">
          <div class="node-dot success"><i class="ri-trophy-line"></i></div>
          <div class="node-content">
            <div class="node-title">结果</div>
            <div class="node-text">Description</div>
            <div class="result-chips">
              <div class="rchip bad"><i class="ri-bug-line"></i>Baseline VALUE</div>
              <div class="rchip ok"><i class="ri-rocket-2-line"></i>Fixed VALUE</div>
            </div>
          </div>
        </div>
        <div class="node-connector">...</div>
        <div class="poster-footer">
          <div class="footer-icon"><i class="ri-brain-line"></i></div>
          <div class="footer-text">
            <div class="footer-title">关注获取更多分析</div>
            <div class="footer-sub">收藏 + 关注</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
```

### CSS (Dark Theme)

```css
.poster-page { background: #0D1117; color: #E6EDF3; }
.poster-bg-grad {
  background: radial-gradient(ellipse at 20% 20%, rgba(9,132,227,0.15) 0%, transparent 50%),
              radial-gradient(ellipse at 80% 80%, rgba(0,184,148,0.1) 0%, transparent 50%);
}
.poster-bg-grid {
  background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 48px 48px;
}
.poster-node {
  display: flex; gap: 12px; padding: 14px 16px;
  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.06);
  border-radius: 14px;
}
.poster-node.danger-node { border-color: rgba(231,76,60,0.2); background: rgba(231,76,60,0.06); }
.poster-node.result-node { border-color: rgba(0,184,148,0.25); background: rgba(0,184,148,0.06); box-shadow: 0 0 24px rgba(0,184,148,0.08); }
.node-dot {
  width: 36px; height: 36px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center; font-size: 18px;
}
.node-dot.accent { background: rgba(9,132,227,0.15); color: #74B9FF; }
.node-dot.success { background: rgba(0,184,148,0.15); color: #34D399; }
.danger-node > .node-dot { background: rgba(231,76,60,0.15); color: #F87171; }
.node-connector { display: flex; flex-direction: column; align-items: center; padding: 3px 0; }
.connector-line { width: 2px; flex: 1; background: rgba(9,132,227,0.2); }
.connector-icon { color: rgba(9,132,227,0.4); font-size: 16px; }
.rchip { display: inline-flex; align-items: center; gap: 3px; padding: 3px 10px; border-radius: 6px; font-size: 12px; font-weight: 600; }
.rchip.bad { background: rgba(231,76,60,0.15); color: #F87171; }
.rchip.ok { background: rgba(0,184,148,0.15); color: #34D399; }
.poster-footer { display: flex; align-items: center; gap: 12px; padding: 14px 16px; background: rgba(255,255,255,0.04); border-radius: 14px; }
.footer-icon {
  width: 40px; height: 40px; border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), #34D399);
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; color: #FFFFFF;
}
@media (max-height: 600px) {
  .poster-node { padding: 4px 6px !important; gap: 6px !important; }
  .node-dot { width: 18px !important; height: 18px !important; font-size: 10px !important; }
  .node-title { font-size: 10px !important; }
  .node-text { font-size: 8px !important; }
}
```
