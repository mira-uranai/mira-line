# -*- coding: utf-8 -*-
"""LPのアイコンの後ろに置く飾りの絵（真ん中は丸く空ける・透過）を gpt-image で3種類作る"""
import base64, io, os
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
load_dotenv(r"C:\Users\ranha\claude\mira-mangetsu\.env")
HERE = os.path.dirname(os.path.abspath(__file__))
REF = "C:/Users/ranha/claude/mira-tokuten/images/mira.png"  # ミラのアイコン（画風と色をそろえる）
COMMON = ("Using the reference illustration ONLY for its painterly Art Nouveau style and soft pastel palette (lavender, pale pink, cream, "
          "muted gold), paint a decorative arrangement that will surround a round portrait on a dark midnight-indigo web page. "
          "The CENTER must be a perfectly circular EMPTY hole, about 56% of the image width, centered, with a clean edge: nothing at all "
          "may enter or overlap the hole. Transparent background outside the painting. Elegant, airy, refined, high-end. "
          "No ring, no frame line, no text, no letters, no person, no face, no glitter, no sparkles, no stars. ")
V = {
    "1_花と三日月": COMMON + "Soft lavender and pale pink lilies, small roses, wisteria and slender leaves arranged ASYMMETRICALLY: "
                    "a lush cluster at the lower left and a smaller one at the upper right, plus a softly glowing pale-gold crescent "
                    "moon at the upper left, partly tucked behind flowers. Lots of breathing room.",
    "2_花のリース": COMMON + "A delicate full wreath of lavender and blush-pink flowers (lilies, roses, small wildflowers) with "
                    "silver-green leaves and a few pearls, light and airy, thinner at the top, fuller at the bottom.",
    "3_月と雲の水彩": COMMON + "A dreamy watercolor halo: soft lavender and pink watercolor clouds swirling around the hole, a large "
                    "pale-gold crescent moon embracing the hole from the left side, a few small pale flowers drifting. Soft edges.",
}
c = OpenAI()
def run(item):
    name, p = item
    with open(REF, "rb") as f:
        r = c.images.edit(model="gpt-image-2.5-sunburst", image=[f], prompt=p, size="1024x1024", n=1,
                          quality="high", background="transparent", output_format="png")
    img = Image.open(io.BytesIO(base64.b64decode(r.data[0].b64_json)))
    img.save(os.path.join(HERE, "deco", f"{name}.png")); return name, img.mode
with ThreadPoolExecutor(3) as ex:
    for res in ex.map(run, V.items()): print(res)
