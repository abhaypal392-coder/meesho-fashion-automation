import csv, os, re, textwrap, requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(ROOT, "products", "products.csv")
OUT = os.path.join(ROOT, "output")
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1350
BG = (255, 247, 250)
INK = (48, 32, 47)
PINK = (228, 65, 126)
MUTED = (110, 92, 106)

def font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def safe_name(s):
    s = re.sub(r"[^a-zA-Z0-9_-]+", "-", s.strip()).strip("-").lower()
    return s[:60] or "product"

def wrap(draw, text, fnt, max_width):
    words, lines, current = str(text).split(), [], ""
    for word in words:
        test = (current + " " + word).strip()
        if draw.textbbox((0,0), test, font=fnt)[2] <= max_width:
            current = test
        else:
            if current: lines.append(current)
            current = word
    if current: lines.append(current)
    return lines

def make_banner(row):
    name = row["product_name"].strip()
    price = row["price_inr"].strip()
    category = row["category"].strip()
    hook = row["hook"].strip() or f"Explore budget {category} finds"
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # Decorative header
    d.rounded_rectangle((48, 48, W-48, 180), radius=36, fill=(255, 226, 238))
    d.text((78, 80), "BUDGET STYLE FINDS", font=font(36, True), fill=INK)
    d.text((80, 132), "FASHION • FINDS • INSPIRATION", font=font(20), fill=MUTED)

    # Product image panel
    panel = (60, 220, W-60, 870)
    d.rounded_rectangle(panel, radius=40, fill=(255,255,255), outline=(241,210,225), width=3)
    image_url = row["image_url"].strip()
    loaded = False
    if image_url.startswith("https://") or image_url.startswith("http://"):
        try:
            resp = requests.get(image_url, timeout=15, headers={"User-Agent":"Mozilla/5.0"})
            resp.raise_for_status()
            product_img = Image.open(BytesIO(resp.content)).convert("RGB")
            product_img.thumbnail((820, 590))
            x = (W-product_img.width)//2
            y = 250 + (580-product_img.height)//2
            img.paste(product_img, (x, y))
            loaded = True
        except Exception:
            pass
    if not loaded:
        d.text((100, 460), "ADD APPROVED PRODUCT IMAGE", font=font(34, True), fill=MUTED)
        d.text((100, 520), "Set a valid image_url in products.csv", font=font(23), fill=MUTED)

    # Hook text
    y = 920
    for line in wrap(d, hook, font(43, True), 930)[:2]:
        d.text((70, y), line, font=font(43, True), fill=INK)
        y += 58
    d.rounded_rectangle((70, 1060, 510, 1160), radius=28, fill=PINK)
    d.text((100, 1083), f"LISTING PRICE: ₹{price}", font=font(27, True), fill=(255,255,255))
    d.text((72, 1200), f"Category: {category}  |  Check current price & details", font=font(21), fill=MUTED)
    d.text((72, 1250), "Affiliate link may earn a commission • Verify details before buying", font=font(18), fill=MUTED)

    out_path = os.path.join(OUT, safe_name(name) + ".jpg")
    img.save(out_path, quality=92, optimize=True)
    return out_path

def main():
    if not os.path.exists(CSV_PATH):
        print("Missing products/products.csv")
        return
    approved = []
    with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row.get("approved","").strip().lower() == "yes":
                if not row.get("affiliate_url","").startswith("http"):
                    print(f"SKIP {row.get('product_name')}: no valid-looking affiliate URL")
                    continue
                approved.append(row)
    if not approved:
        print("No approved products found. Add verified products and set approved=yes.")
        return

    lines = ["# Daily creative report", "", "Review every creative and verify product details before posting.", ""]
    for row in approved:
        path = make_banner(row)
        caption = (
            f"{row['hook'].strip() or row['product_name']}\\n\\n"
            f"Listed price: ₹{row['price_inr']} (check current listing price and availability).\\n"
            f"Product: {row['product_name']}\\n"
            f"Affiliate link: {row['affiliate_url']}\\n\\n"
            "#BudgetFashion #FashionFinds #IndianFashion\\n"
            "Disclosure: This post may contain an affiliate link; I may earn a commission from eligible purchases."
        )
        txt_path = os.path.splitext(path)[0] + ".txt"
        with open(txt_path, "w", encoding="utf-8") as out:
            out.write(caption)
        lines.append(f"- **{row['product_name']}** — banner: `{os.path.basename(path)}`, caption: `{os.path.basename(txt_path)}`")
    with open(os.path.join(OUT, "REPORT.md"), "w", encoding="utf-8") as f:
        f.write("\\n".join(lines))
    print(f"Created {len(approved)} creative(s) in output/")

if __name__ == "__main__":
    main()
