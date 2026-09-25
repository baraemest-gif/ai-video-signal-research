#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets" / "hvac-cover.png"
OUT.parent.mkdir(parents=True, exist_ok=True)

W,H = 2000,1600
img = Image.new("RGB",(W,H),(14,31,53))
d = ImageDraw.Draw(img)

def font(size,bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p,size)
    return ImageFont.load_default()

white=(255,255,255)
accent=(62,197,205)
soft=(214,226,236)

d.rounded_rectangle((90,85,1910,1515),radius=48,outline=(52,79,105),width=4)
d.text((140,150),"JOYPRINT17",font=font(54,True),fill=accent)
d.text((140,300),"HVAC BUSINESS",font=font(145,True),fill=white)
d.text((140,465),"GROWTH &",font=font(130,True),fill=accent)
d.text((140,610),"OPERATIONS KIT",font=font(130,True),fill=white)
d.text((145,820),"18 EDITABLE CANVA TEMPLATES",font=font(60,True),fill=soft)

bullets = [
    "Estimates & client forms",
    "Job & quality checklists",
    "Flyer + door hanger",
    "Social media + local marketing",
    "SMS / email scripts + KPI tracker",
]
y=950
for item in bullets:
    d.ellipse((150,y+14,176,y+40),fill=accent)
    d.text((205,y),item,font=font(43),fill=white)
    y += 95

d.rounded_rectangle((140,1430,840,1510),radius=20,fill=accent)
d.text((178,1443),"DIGITAL DOWNLOAD • CANVA",font=font(34,True),fill=(9,31,45))

img.save(OUT,optimize=True)
print(f"COVER_READY={OUT}")
