#!/usr/bin/env python3
"""
html2carousel.py -- HTML to Social Media Carousel Image Converter

Converts HTML slide presentations to individual PNG/JPG images
for social media platforms (Xiaohongshu, WeChat, Instagram, etc.).

Pipeline:
    Mode A: HTML -> Playwright screenshots -> individual PNG/JPG images
    Mode B: User images + text overlay (from _carousel_design.json) -> composite images

Usage:
    python html2carousel.py input.html
    python html2carousel.py input.html -o output/ --format jpg --caption
    python html2carousel.py --images-dir ./photos/ --overlay-text design.json -o output/
"""

import argparse
import json
import os
import re
import sys
import textwrap
import shutil
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Error: pillow not installed. Run: pip install pillow")

DEFAULT_WIDTH = 1080
DEFAULT_HEIGHT = 1440
DEFAULT_FONT = (
    "C:/Windows/Fonts/msyh.ttc"
    if sys.platform == "win32"
    else "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
)
SAFE_TOP = 120
SAFE_BOTTOM = 180
SAFE_SIDE = 60


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert HTML slides to social media carousel images"
    )

    mode_a = parser.add_argument_group("Mode A: HTML -> Images")
    mode_a.add_argument("input", nargs="?", default=None, help="Input HTML file path")
    mode_a.add_argument(
        "-o", "--output", default="./carousel_output/", help="Output directory (default: ./carousel_output/)"
    )
    mode_a.add_argument(
        "--width", type=int, default=DEFAULT_WIDTH, help=f"Image width (default: {DEFAULT_WIDTH})"
    )
    mode_a.add_argument(
        "--height", type=int, default=DEFAULT_HEIGHT, help=f"Image height (default: {DEFAULT_HEIGHT})"
    )
    mode_a.add_argument(
        "--slide-selector", default=".slide", help="CSS selector for slides (default: .slide)"
    )
    mode_a.add_argument(
        "--format", default="png", choices=["png", "jpg"], help="Output format (default: png)"
    )
    mode_a.add_argument(
        "--quality", type=int, default=95, help="JPG quality 1-100 (default: 95)"
    )
    mode_a.add_argument(
        "--prefix", default="carousel", help="Filename prefix (default: carousel)"
    )
    mode_a.add_argument(
        "--caption", action="store_true", help="Generate _post_text.txt with social media caption"
    )
    mode_a.add_argument(
        "--platform", default="xiaohongshu",
        choices=["xiaohongshu", "instagram", "wechat", "general"],
        help="Target platform (default: xiaohongshu)"
    )
    mode_a.add_argument(
        "--json", default=None, help="Path to _carousel_design.json for metadata"
    )

    mode_b = parser.add_argument_group("Mode B: Images + Text Overlay")
    mode_b.add_argument(
        "--images-dir", default=None,
        help="Directory containing source images for Mode B"
    )
    mode_b.add_argument(
        "--overlay-text", default=None,
        help="Path to _carousel_design.json with text content per page"
    )
    mode_b.add_argument(
        "--font", default=DEFAULT_FONT, help="Font path for text overlay"
    )

    return parser.parse_args()


def read_html(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()


def inject_slide_nav_js(html_content, selector=".slide"):
    nav_js = f"""
<script>
function getSlideElements() {{
    var container = document.querySelector('.carousel') || document.querySelector('.slide-container');
    if (container) {{
        return container.querySelectorAll(':scope > .slide');
    }}
    return document.querySelectorAll('{selector}');
}}
window.__totalSlides = getSlideElements().length;
window.__currentSlide = 0;
function goToSlide(n) {{
    var slides = getSlideElements();
    for (var i = 0; i < slides.length; i++) {{
        slides[i].style.display = (i === n) ? 'block' : 'none';
    }}
    window.__currentSlide = n;
}}
function getSlideText(n) {{
    var slides = getSlideElements();
    if (n < slides.length) {{
        return slides[n].innerText.trim();
    }}
    return '';
}}
goToSlide(0);
</script>
"""
    if "</body>" in html_content:
        html_content = html_content.replace("</body>", nav_js + "\n</body>")
    else:
        html_content += nav_js
    return html_content


def screenshot_slides_sync(html_path, output_dir, width, height, selector=".slide", prefix="carousel", fmt="png", quality=95):
    from playwright.sync_api import sync_playwright

    html_content = read_html(html_path)
    html_content = inject_slide_nav_js(html_content, selector)
    modified_path = os.path.join(output_dir, "_modified.html")
    with open(modified_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    screenshots = []
    slide_texts = []
    file_url = Path(modified_path).as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(file_url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(1000)

        total_slides = page.evaluate("window.__totalSlides || 0")

        if total_slides > 0:
            for slide_idx in range(total_slides):
                page.evaluate(f"goToSlide({slide_idx})")
                page.wait_for_timeout(300)
                text = page.evaluate(f"getSlideText({slide_idx})")
                slide_texts.append(text)

                ext = "jpg" if fmt == "jpg" else "png"
                out_path = os.path.join(output_dir, f"{prefix}_{slide_idx + 1:03d}.{ext}")
                shot_kwargs = {"path": out_path, "type": "jpeg" if fmt == "jpg" else "png"}
                if fmt == "jpg":
                    shot_kwargs["quality"] = quality
                page.screenshot(**shot_kwargs)
                screenshots.append(out_path)
                print(f"  [OK] Slide {slide_idx + 1}/{total_slides}: {os.path.basename(out_path)}")
        else:
            text = page.evaluate("document.body.innerText.trim()")
            slide_texts.append(text)
            ext = "jpg" if fmt == "jpg" else "png"
            out_path = os.path.join(output_dir, f"{prefix}_001.{ext}")
            page.screenshot(path=out_path)
            screenshots.append(out_path)

        browser.close()

    return screenshots, slide_texts


def _wrap_text_for_overlay(text, font, max_width, max_lines=8):
    lines = []
    cur = ""
    for ch in text:
        test = cur + ch
        bb = font.getbbox(test)
        if bb[2] - bb[0] > max_width:
            if cur:
                lines.append(cur)
            cur = ch
            if len(lines) >= max_lines:
                lines[-1] = lines[-1].rstrip() + "..."
                break
        else:
            cur = test
    if cur and len(lines) < max_lines:
        lines.append(cur)
    return lines if lines else [text[:20]]


def overlay_text_on_image(img_path, title, subtitle, body, page_num, total_pages, output_path, font_path, width, height):
    img = Image.open(img_path).convert("RGBA")
    img = img.resize((width, height), Image.LANCZOS)

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    content_x = SAFE_SIDE
    content_y = SAFE_TOP
    content_w = width - 2 * SAFE_SIDE

    y = content_y

    if title:
        title_fs = min(72, int(width * 0.065))
        try:
            title_font = ImageFont.truetype(font_path, title_fs)
        except Exception:
            title_font = ImageFont.load_default()
        tlines = _wrap_text_for_overlay(title, title_font, content_w, max_lines=2)
        for line in tlines:
            draw.text((content_x + 2, y + 2), line, fill=(0, 0, 0, 160), font=title_font)
            draw.text((content_x, y), line, fill=(45, 32, 22, 255), font=title_font)
            bb = title_font.getbbox(line)
            y += (bb[3] - bb[1]) + 16
        y += 12

    if subtitle:
        sub_fs = min(40, int(width * 0.037))
        try:
            sub_font = ImageFont.truetype(font_path, sub_fs)
        except Exception:
            sub_font = ImageFont.load_default()
        slines = _wrap_text_for_overlay(subtitle, sub_font, content_w, max_lines=2)
        for line in slines:
            draw.text((content_x, y), line, fill=(139, 115, 85, 230), font=sub_font)
            bb = sub_font.getbbox(line)
            y += (bb[3] - bb[1]) + 10
        y += 12

    if body:
        body_fs = min(32, int(width * 0.030))
        try:
            body_font = ImageFont.truetype(font_path, body_fs)
        except Exception:
            body_font = ImageFont.load_default()
        blines = _wrap_text_for_overlay(body, body_font, content_w, max_lines=12)
        for line in blines:
            draw.text((content_x, y), line, fill=(60, 60, 60, 240), font=body_font)
            bb = body_font.getbbox(line)
            y += (bb[3] - bb[1]) + 8

    if page_num is not None and total_pages is not None:
        indicator_fs = 20
        try:
            ind_font = ImageFont.truetype(font_path, indicator_fs)
        except Exception:
            ind_font = ImageFont.load_default()
        ind_text = f"{page_num}/{total_pages}"
        bb = ind_font.getbbox(ind_text)
        ind_w = bb[2] - bb[0]
        ind_x = width - SAFE_SIDE - ind_w
        ind_y = height - SAFE_BOTTOM + 20
        draw.text((ind_x, ind_y), ind_text, fill=(160, 160, 160, 200), font=ind_font)

    result = Image.alpha_composite(img, overlay)
    result = result.convert("RGB")
    result.save(output_path, quality=95)
    return output_path


def generate_post_caption(slide_texts, carousel_data=None):
    first_text = slide_texts[0] if slide_texts else ""
    title = first_text.strip().replace("\n", " ")[:50]

    body_parts = []
    for t in slide_texts[1:]:
        cleaned = t.strip().replace("\n", " ")
        if cleaned:
            body_parts.append(cleaned[:60])

    body = "\n".join(body_parts[:3])
    if len(body) > 200:
        body = body[:197] + "..."

    caption = f"""{title}

{body}

#生活分享 #干货 #小技巧 #自我提升 #生活方式

你觉得哪一条最有用？评论区告诉我吧~
"""
    return caption


def generate_cover_thumbnail(first_image, output_path):
    if not os.path.exists(first_image):
        return None
    img = Image.open(first_image)
    thumb_size = (300, 400)
    img = img.resize(thumb_size, Image.LANCZOS)
    img.save(output_path, quality=95)
    return output_path


def mode_a_html_to_images(args):
    if not args.input:
        sys.exit("Error: Input HTML file required for Mode A")
    html_path = os.path.abspath(args.input)
    if not os.path.exists(html_path):
        sys.exit(f"Error: Input file not found: {html_path}")

    output_dir = os.path.abspath(args.output)
    os.makedirs(output_dir, exist_ok=True)

    print(f"[INFO] Input:    {html_path}")
    print(f"[INFO] Output:   {output_dir}")
    print(f"[INFO] Size:     {args.width}x{args.height}")
    print(f"[INFO] Format:   {args.format.upper()}")
    print(f"[INFO] Platform: {args.platform}")

    print("\n[PHASE 1] Screenshots...")
    screenshots, slide_texts = screenshot_slides_sync(
        html_path, output_dir, args.width, args.height,
        args.slide_selector, args.prefix, args.format, args.quality
    )
    total = len(screenshots)
    print(f"[OK] {total} images generated")

    if screenshots:
        cover_path = os.path.join(output_dir, "carousel_cover.png")
        generate_cover_thumbnail(screenshots[0], cover_path)
        print(f"[OK] Cover thumbnail: {cover_path}")

    if args.caption:
        carousel_data = None
        if args.json and os.path.exists(args.json):
            with open(args.json, "r", encoding="utf-8") as f:
                carousel_data = json.load(f)
        caption = generate_post_caption(slide_texts, carousel_data)
        caption_path = os.path.join(output_dir, "_post_text.txt")
        with open(caption_path, "w", encoding="utf-8") as f:
            f.write(caption)
        print(f"[OK] Post caption: {caption_path}")

    print(f"\n[DONE] {total} carousel images saved to: {output_dir}")
    return screenshots


def mode_b_images_with_overlay(args):
    if not args.overlay_text:
        sys.exit("Error: Mode B requires --overlay-text (path to _carousel_design.json)")
    if not args.images_dir:
        sys.exit("Error: Mode B requires --images-dir")

    json_path = os.path.abspath(args.overlay_text)
    images_dir = os.path.abspath(args.images_dir)
    output_dir = os.path.abspath(args.output)
    os.makedirs(output_dir, exist_ok=True)

    with open(json_path, "r", encoding="utf-8") as f:
        design = json.load(f)

    pages = design.get("pages", [])
    width = design.get("resolution", {}).get("width", args.width)
    height = design.get("resolution", {}).get("height", args.height)
    total_pages = len(pages)

    image_files = sorted(
        [f for f in os.listdir(images_dir) if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))]
    )

    if not image_files:
        sys.exit(f"Error: No images found in {images_dir}")

    print(f"[MODE B] Images:   {len(image_files)} files")
    print(f"[MODE B] Pages:    {total_pages} in design")
    print(f"[MODE B] Output:   {output_dir}")

    outputs = []
    for i, page in enumerate(pages):
        img_idx = min(i, len(image_files) - 1)
        img_path = os.path.join(images_dir, image_files[img_idx])

        title = page.get("title", "")
        subtitle = page.get("subtitle", "")
        body = page.get("body", "")
        page_num = i + 1 if i > 0 else None

        out_name = f"{args.prefix}_{i + 1:03d}.png"
        out_path = os.path.join(output_dir, out_name)

        overlay_text_on_image(
            img_path, title, subtitle, body,
            page_num, total_pages,
            out_path, args.font, width, height
        )
        outputs.append(out_path)
        print(f"  [OK] Page {i + 1}/{total_pages}: {out_name}")

    if outputs:
        cover_path = os.path.join(output_dir, "carousel_cover.png")
        generate_cover_thumbnail(outputs[0], cover_path)
        print(f"[OK] Cover thumbnail: {cover_path}")

    print(f"\n[DONE] {len(outputs)} composite images saved to: {output_dir}")
    return outputs


def main():
    args = parse_args()

    if args.images_dir or args.overlay_text:
        mode_b_images_with_overlay(args)
    elif args.input:
        mode_a_html_to_images(args)
    else:
        sys.exit("Error: Provide input HTML file (Mode A) or --images-dir + --overlay-text (Mode B)")


if __name__ == "__main__":
    main()
