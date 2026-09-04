from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
CERT_DIR = ROOT / "assets" / "images" / "certificates"
OUT_DIR = ROOT / "assets" / "images" / "misc"
OUT_PATH = OUT_DIR / "awards_summary_collage_2026_08.jpg"

FONT_REG = "C:/Windows/Fonts/msyh.ttc"
FONT_BOLD = "C:/Windows/Fonts/msyhbd.ttc"


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def prepare_certificate(path):
    img = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    if path.name == "马皓然国家奖学金荣誉证书.jpg":
        img = img.rotate(90, expand=True)
    return img


def fit_contain(img, size):
    img.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", size, "white")
    x = (size[0] - img.width) // 2
    y = (size[1] - img.height) // 2
    canvas.paste(img, (x, y))
    return canvas


def card(draw, xy, fill="#fffdf8", outline="#ded2bc"):
    draw.rounded_rectangle(xy, radius=8, fill=fill, outline=outline, width=2)


priority = [
    "马皓然国家奖学金荣誉证书.jpg",
    "2026ROBOCON正赛一等奖.jpg",
    "2026ROBOCON任务赛一一等奖.jpg",
    "2026ROBOCON任务赛二二等奖.jpg",
    "2026ROBOCON个人一等奖.jpg",
    "2026ROBOCON个人三等奖.jpg",
    "2026ROBOCON四足挑战赛一等奖.jpg",
    "2026ROBOCON四足挑战赛二等奖.jpg",
    "2026ROBOCON人形功夫搏击赛大型组三等奖.jpg",
    "2026网数智安全大赛作品赛二等奖.jpg",
    "ROBOCON飞身上篮竞技赛一等奖.jpg",
    "ROBOCON飞身上篮全能奖.jpg",
    "ROBOCON排球挑战赛一等奖.jpg",
    "ROBOCON技能挑战赛投篮一等奖.jpg",
    "ROBOCON技能挑战赛运球一等奖.jpg",
    "ROBOCON四足竞速赛二等奖.jpg",
    "ROBOCON四足越野赛二等奖.jpg",
    "ROBOCON四足障碍赛三等奖.jpg",
    "2025中国机器人大赛暨RoboCup机器人世界杯中国赛（中国机器人大赛赛区）-水下机器人-水中作业项目（总决赛）-Y2509T1449769-传奇战神龙王队获奖证书.jpg",
    "2024RoCupAUV赛道国赛三等奖.jpg",
    "RST水下作业国赛三等奖.jpg",
    "RST水下作业赛陕西赛区二等奖.jpg",
    "RST目标抓取国赛三等奖.jpg",
    "RST目标抓取赛陕西赛区二等奖.jpg",
    "中国机器人及人工智能大赛省级二等奖.jpg",
]

files = [CERT_DIR / name for name in priority if (CERT_DIR / name).exists()]

W, H = 3840, 2160
img = Image.new("RGB", (W, H), "#f7f4ed")
draw = ImageDraw.Draw(img)

for i, color in enumerate(["#e9dcc8", "#d6e7e4", "#f1c8b6"]):
    x0 = -360 + i * 900
    draw.polygon([(x0, 0), (x0 + 980, 0), (x0 + 560, H), (x0 - 420, H)], fill=color)

overlay = Image.new("RGBA", (W, H), (247, 244, 237, 218))
img = Image.alpha_composite(img.convert("RGBA"), overlay)
draw = ImageDraw.Draw(img)

grid_x, grid_y = 120, 92
gap_x, gap_y = 28, 26
cell_w = (W - 2 * grid_x - 4 * gap_x) // 5
cell_h = (H - grid_y - 80 - 4 * gap_y) // 5
thumb_w = cell_w - 72
thumb_h = cell_h - 42

for idx, path in enumerate(files):
    row, col = divmod(idx, 5)
    x = grid_x + col * (cell_w + gap_x)
    y = grid_y + row * (cell_h + gap_y)

    shadow = Image.new("RGBA", (cell_w + 28, cell_h + 28), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((14, 14, cell_w + 10, cell_h + 10), radius=8, fill=(38, 50, 56, 34))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    img.alpha_composite(shadow, (x - 12, y - 10))

    card(draw, (x, y, x + cell_w, y + cell_h))
    cert = fit_contain(prepare_certificate(path), (thumb_w, thumb_h))
    px = x + (cell_w - thumb_w) // 2
    py = y + (cell_h - thumb_h) // 2
    img.paste(cert, (px, py))

OUT_DIR.mkdir(parents=True, exist_ok=True)
img.convert("RGB").save(OUT_PATH, "JPEG", quality=92, optimize=True)
print(OUT_PATH)
print(f"{OUT_PATH.stat().st_size / 1024 / 1024:.2f} MB")
