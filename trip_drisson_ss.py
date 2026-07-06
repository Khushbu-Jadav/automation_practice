from DrissionPage import ChromiumPage
import time
import json
from PIL import Image
import io
import os
import re

browser = ChromiumPage()
page = browser.latest_tab

os.makedirs("screenshots", exist_ok=True)

with open("hotel_links1.json", "r", encoding='utf-8') as f:
    data = json.load(f)

def file_name(name):
    return re.sub(r"[^\w-]", "_", name.strip())

for hotel in data:
    hotel_id = hotel["hotel_id"]
    hotel_name = hotel["hotel_name"]
    hotel_url = hotel["hotel_url"]

    page.get(hotel_url)

    spans = page.eles("xpath://span[@class='foldButton-fold_text__xsBlX']")
    for span in spans:
        try:
            span.click()
            time.sleep(0.3)
        except Exception:
            continue

    view_height_css = page.run_js("return window.innerHeight;")
    dpi_scale = page.run_js("return window.devicePixelRatio || 1;")
    view_height_pixels = int(view_height_css * dpi_scale)

    current_scroll_css = 0
    screenshots = []

    print(f"Viewport CSS Height: {view_height_css}px | DPI Scale: {dpi_scale}x")

    while True:
        total_height_css = page.run_js("return document.documentElement.scrollHeight;")

        print(f"Scrolling to: {current_scroll_css}px / {total_height_css}px")
        page.run_js(f"window.scrollTo(0, {current_scroll_css});")
        time.sleep(0.4)

        img_bytes = page.get_screenshot(as_bytes='png')
        img = Image.open(io.BytesIO(img_bytes))

        if current_scroll_css + view_height_css >= total_height_css:
            remaining_height_css = total_height_css - current_scroll_css
            remaining_height_pixels = int(remaining_height_css * dpi_scale)
            overlap_height_pixels = view_height_pixels - remaining_height_pixels

            if remaining_height_pixels > 0:
                img = img.crop((0, overlap_height_pixels, img.width, view_height_pixels))
                screenshots.append(img)
            break

        screenshots.append(img)
        current_scroll_css += view_height_css

    total_width = screenshots[0].width
    final_height_pixels = sum(s.height for s in screenshots)
    final_image = Image.new('RGB', (total_width, final_height_pixels))

    y_offset = 0
    for stitch_img in screenshots:
        final_image.paste(stitch_img, (0, y_offset))
        y_offset += stitch_img.height

    out_path = f"screenshots/{file_name(hotel_name)}_{hotel_id}.png"
    final_image.save(out_path)
    print(f"Saved: {out_path}")

    time.sleep(2)

browser.quit()