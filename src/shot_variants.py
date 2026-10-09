# -*- coding: utf-8 -*-
"""アイコン装飾の案（src/variants/*.html）を撮って、1枚の比較画像にする"""
import glob, pathlib
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
SCR = pathlib.Path(r"C:/Users/ranha/AppData/Local/Temp/claude/C--Users-ranha/9da1badd-1630-46e9-83d2-a9492bc65b4e/scratchpad")
fs = sorted(glob.glob("src/variants/*.html"))
shots = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for f in fs:
        pg = b.new_page(viewport={"width": 390, "height": 700}, device_scale_factor=2)
        pg.goto(pathlib.Path(f).resolve().as_uri()); pg.wait_for_timeout(1500)
        out = SCR / f"v_{len(shots)}.png"; pg.screenshot(path=str(out)); shots.append((pathlib.Path(f).stem, out))
    b.close()
W = 780
sheet = Image.new("RGB", (W * len(shots) + 20 * (len(shots) + 1), 1400 + 110), (240, 236, 244))
fnt = ImageFont.truetype("C:/Users/ranha/claude/mira-story/fonts/ZenKakuGothicNew-Bold.ttf", 48)
dr = ImageDraw.Draw(sheet)
for i, (n, f) in enumerate(shots):
    x = 20 + i * (W + 20)
    sheet.paste(Image.open(f), (x, 100)); dr.text((x + 10, 25), n.replace("_", "："), font=fnt, fill=(60, 40, 80))
sheet.save("C:/Users/ranha/Pictures/ミラLP_アイコン案.png")
sheet.resize((sheet.width // 3, sheet.height // 3)).save(SCR / "v_sheet.png")
print([s[0] for s in shots])
