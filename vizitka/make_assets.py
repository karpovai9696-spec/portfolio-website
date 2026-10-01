import os
import re
import urllib.request

import qrcode

MEDIA = "vizitka/media"
FONTS = "vizitka/fonts"
os.makedirs(MEDIA, exist_ok=True)
os.makedirs(FONTS, exist_ok=True)

# 1) QR code on white card (quiet zone included)
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=12, border=2)
qr.add_data("https://yq2no6cpbdyom.kimi.page")
qr.make(fit=True)
img = qr.make_image(fill_color="#0B0D12", back_color="white")
img.save(os.path.join(MEDIA, "qr.png"))
print("QR saved:", img.size)

# 2) Fonts (TTF via legacy Google Fonts API)
def fetch_font(family_query, out_name):
    url = f"https://fonts.googleapis.com/css?family={family_query}"
    req = urllib.request.Request(url, headers={"User-Agent": "curl/7.0"})
    css = urllib.request.urlopen(req, timeout=30).read().decode()
    m = re.search(r"url\((https://[^)]+\.ttf)\)", css)
    if not m:
        raise RuntimeError(f"no ttf in css for {family_query}: {css[:200]}")
    req2 = urllib.request.Request(m.group(1), headers={"User-Agent": "curl/7.0"})
    data = urllib.request.urlopen(req2, timeout=60).read()
    path = os.path.join(FONTS, out_name)
    with open(path, "wb") as f:
        f.write(data)
    print(out_name, len(data), "bytes")

fetch_font("Russo+One", "RussoOne.ttf")
fetch_font("Manrope:wght@400", "Manrope-Regular.ttf")
fetch_font("Manrope:wght@600", "Manrope-SemiBold.ttf")
fetch_font("Manrope:wght@800", "Manrope-ExtraBold.ttf")
fetch_font("JetBrains+Mono:wght@500", "JetBrainsMono-Medium.ttf")
