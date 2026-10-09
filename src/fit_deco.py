# -*- coding: utf-8 -*-
"""飾りの絵の「空いた丸」の中心と半径を測り、LPに使う画像（webp）と比較用HTMLを作る"""
import glob, json, os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
base = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
info = {}
for path in sorted(glob.glob(os.path.join(HERE, "deco", "*.png"))):
    name = os.path.splitext(os.path.basename(path))[0]
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im.resize((256, 256)))[:, :, 3] > 40
    ys, xs = np.nonzero(a)
    best = (0, 128, 128)
    for cy in range(100, 157, 2):
        for cx in range(100, 157, 2):
            r = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2).min()
            if r > best[0]:
                best = (r, cx, cy)
    r, cx, cy = [v * 4 for v in best]
    info[name] = {"cx": cx / 1024, "cy": cy / 1024, "r": r / 1024}
    im.resize((640, 640), Image.LANCZOS).save(os.path.join(ROOT, "images", f"deco_{name[0]}.webp"), quality=88)
    # 比較用HTML：飾り 300px 四方、アイコンは空いた丸の 92%（すき間を残す）
    S = 300
    d = 2 * r / 1024 * S * .92
    css = (f"  .portrait {{ position: relative; width: {S}px; height: {S}px; margin: -30px auto -10px; }}\n"
           f"  .portrait .deco {{ position: absolute; inset: 0; width: 100%; height: 100%; }}\n"
           f"  .portrait .icon {{ position: absolute; left: {cx/1024*100:.2f}%; top: {cy/1024*100:.2f}%; width: {d:.0f}px; height: {d:.0f}px; "
           f"transform: translate(-50%, -50%); border-radius: 50%; object-fit: cover; box-shadow: 0 16px 30px -14px rgba(0,0,0,.8); }}\n")
    s = base
    ca = s.index("  .portrait {"); cb = s.index("  .portrait .icon {"); cb = s.index("\n", s.index("}", cb)) + 1
    s = s[:ca] + css + s[cb:]
    s = s.replace('        <img class="icon"', f'        <img class="deco" src="images/deco_{name[0]}.webp" alt="" aria-hidden="true">\n        <img class="icon"')
    s = s.replace("images/", "../../images/")
    open(os.path.join(HERE, "variants", f"{name}.html"), "w", encoding="utf-8").write(s)
json.dump(info, open(os.path.join(HERE, "deco", "holes.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps(info, ensure_ascii=False))
