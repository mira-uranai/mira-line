# -*- coding: utf-8 -*-
"""LINE中継ページのヒーロー画像（ミラ＋夜空＋金の装飾）を gpt-image で作る"""
import base64, io, os
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
load_dotenv(r"C:\Users\ranha\claude\mira-mangetsu\.env")
HERE = os.path.dirname(os.path.abspath(__file__))
REF = r"C:\Users\ranha\claude\mira-tokuten\images\mira.png"
P = ("Using the reference image for the character (the same woman: Mira, a gentle fortune teller with wavy auburn hair, "
     "lavender dress, glowing crystal ball), create a luxurious, enchanting vertical hero illustration for a mobile web page. "
     "Art Nouveau / Mucha-inspired painterly style, elegant and dreamy. Mira is in the upper-center, shown from the chest up, "
     "softly smiling and gazing gently toward the viewer, both hands around a glowing pink-gold crystal ball. "
     "Behind her: a deep midnight indigo-violet night sky full of tiny twinkling stars, a large luminous crescent moon, "
     "and an ornate golden Art Nouveau arch / halo frame with delicate flourishes, stars and small pearls. "
     "Soft lavender and rose light, gold shimmer particles floating. "
     "The bottom 35% of the image fades smoothly into a plain, dark midnight indigo (#1a1330) with only faint stars, "
     "calm and empty so text can be placed over it. "
     "No text, no letters, no logo, no watermark.")
c = OpenAI()
for i in range(2):
    with open(REF, "rb") as f:
        r = c.images.edit(model="gpt-image-2.5-sunburst", image=[f], prompt=P, size="1088x1360", n=1, quality="high")
    img = Image.open(io.BytesIO(base64.b64decode(r.data[0].b64_json))).convert("RGB")
    img.save(os.path.join(HERE, f"hero_raw_{i}.png")); print("ok", i, img.size)
