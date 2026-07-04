#!/usr/bin/env python3
"""
Memotest Bug Hunter – PDF Generator
====================================
Generates a print-ready 2-page A4 PDF:
  Page 1 – all card fronts (real insect photos, 36 unique bugs × 2 = 72 cards)
  Page 2 – all card backs  (uniform Bug Hunter pattern, same grid)

Optimised for duplex (long-edge flip) printing: cut on the dashed guide lines.
No titles or instructions are included on the cards.
"""

import os, math, time, requests, tempfile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as rl_canvas

# ---------------------------------------------------------------------------
# 0.  Config
# ---------------------------------------------------------------------------
CACHE_DIR   = os.path.join(os.path.dirname(__file__), "img_cache")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "memotest_bug_hunter.pdf")
os.makedirs(CACHE_DIR, exist_ok=True)

MARGIN_MM  = 6.0     # outer margin (all sides)
GAP_MM     = 1.5     # gap between cards (cut-guide space)
TARGET_DPI = 300

# ---------------------------------------------------------------------------
# 1.  36 insects  →  72 cards  (each appears exactly twice)
#     Tuples: (spanish_name, scientific_name_for_inat_search)
# ---------------------------------------------------------------------------
INSECTS = [
    # Row 1 equivalents
    ("Vaquita",           "Coccinella septempunctata"),
    ("Abeja miel",        "Apis mellifera"),
    ("Mariposa monarca",  "Danaus plexippus"),
    ("Mariposa azul",     "Morpho peleides"),
    ("Saltamontes verde", "Locusta migratoria"),
    ("Escarabajo ciervo", "Lucanus cervus"),
    ("Chinche verde",     "Palomena prasina"),
    ("Hormiga colorada",  "Formica rufa"),
    # Row 2 equivalents
    ("Escarabajo tierra", "Carabus violaceus"),
    ("Hormiga negra",     "Lasius niger"),
    ("Libélula roja",     "Sympetrum vulgatum"),
    ("Mantis religiosa",  "Mantis religiosa"),
    ("Abejorro",          "Bombus terrestris"),
    ("Oruga",             "Papilio machaon"),
    ("Mosca azul",        "Calliphora vicina"),
    ("Libélula azul",     "Libellula depressa"),
    # Row 3 equivalents
    ("Escarabajo rojo",   "Pyrochroa coccinea"),
    ("Abeja solitar.",    "Osmia bicornis"),
    ("Langosta",          "Schistocerca gregaria"),
    ("Caracol jardín",    "Cornu aspersum"),
    ("Insecto palo",      "Carausius morosus"),
    ("Chinche grande",    "Nezara viridula"),
    ("Luciérnaga",        "Lampyris noctiluca"),
    ("Lombriz",           "Lumbricus terrestris"),
    # Row 4 equivalents
    ("Araña jardín",      "Araneus diadematus"),
    ("Cochinilla",        "Armadillidium vulgare"),
    ("Escarabajo negro",  "Pterostichus melanarius"),
    ("Polilla",           "Noctua pronuba"),
    ("Ciempiés",          "Scolopendra cingulata"),
    ("Mosca doméstica",   "Musca domestica"),
    ("Escorpión",         "Pandinus imperator"),
    # Row 5 equivalents
    ("Langosta marrón",   "Acridium aegyptium"),
    ("Chinche de fuego",  "Pyrrhocoris apterus"),
    ("Avispa",            "Vespula vulgaris"),
    ("Babosa",            "Limax maximus"),
    ("Grillo",            "Gryllus bimaculatus"),
]

assert len(INSECTS) == 36, f"Expected 36 insects, got {len(INSECTS)}"
TOTAL_CARDS = len(INSECTS) * 2       # 72

# ---------------------------------------------------------------------------
# 2.  Compute optimal grid   (maximise card area for TOTAL_CARDS on A4)
# ---------------------------------------------------------------------------
A4_W_MM, A4_H_MM = 210.0, 297.0

def best_grid(n, pw, ph, mg, gap):
    """Return (cols, rows, cw, ch) maximising card area."""
    best, best_area = None, 0
    for cols in range(1, n + 1):
        rows = math.ceil(n / cols)
        cw = (pw - 2*mg - (cols-1)*gap) / cols
        ch = (ph - 2*mg - (rows-1)*gap) / rows
        if cw <= 0 or ch <= 0:
            continue
        area = cw * ch
        if area > best_area:
            best_area = area
            best = (cols, rows, cw, ch)
    return best

COLS, ROWS, CARD_W_MM, CARD_H_MM = best_grid(
    TOTAL_CARDS, A4_W_MM, A4_H_MM, MARGIN_MM, GAP_MM
)
print(f"Grid: {COLS}×{ROWS}  |  card: {CARD_W_MM:.2f}×{CARD_H_MM:.2f} mm  "
      f"  ({COLS*ROWS} slots for {TOTAL_CARDS} cards)")

def mm2pt(x): return x * 72.0 / 25.4
def mm2px(x): return int(round(x / 25.4 * TARGET_DPI))

CARD_W_PX = mm2px(CARD_W_MM)
CARD_H_PX = mm2px(CARD_H_MM)
print(f"Card pixels at {TARGET_DPI} DPI: {CARD_W_PX}×{CARD_H_PX}")

# ---------------------------------------------------------------------------
# 3.  Image download helpers
# ---------------------------------------------------------------------------
INAT_API = "https://api.inaturalist.org/v1/taxa"
HDR      = {"User-Agent": "BugHunterMemotest/1.0 (educational print project)"}

def inat_photo_url(scientific_name: str) -> str | None:
    try:
        r = requests.get(INAT_API,
                         params={"q": scientific_name, "limit": 1},
                         headers=HDR, timeout=12)
        r.raise_for_status()
        for result in r.json().get("results", []):
            photo = result.get("default_photo") or {}
            url = photo.get("medium_url") or photo.get("url")
            if url:
                return url
    except Exception as e:
        print(f"    iNat error for {scientific_name!r}: {e}")
    return None


def fetch_image(url: str) -> Image.Image | None:
    try:
        r = requests.get(url, headers=HDR, timeout=15)
        r.raise_for_status()
        return Image.open(BytesIO(r.content)).convert("RGBA")
    except Exception as e:
        print(f"    fetch error {url}: {e}")
        return None


def load_insect(name_es: str, sci_name: str) -> Image.Image:
    cache_file = os.path.join(CACHE_DIR, f"{sci_name.replace(' ','_')}.png")
    if os.path.exists(cache_file):
        return Image.open(cache_file).convert("RGBA")

    print(f"  Downloading: {sci_name} …")
    photo_url = inat_photo_url(sci_name)
    if photo_url:
        img = fetch_image(photo_url)
        if img:
            img.save(cache_file)
            time.sleep(0.4)   # polite rate limit
            return img

    time.sleep(0.4)
    return None

# ---------------------------------------------------------------------------
# 4.  Card design helpers
# ---------------------------------------------------------------------------
CARD_BG    = (253, 250, 240, 255)    # warm parchment
BORDER_COL = (180, 155, 110, 255)    # golden-tan border
TEXT_COL   = (60,  45,  25, 255)     # dark brown text

try:
    FONT_BIG   = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        max(8, CARD_W_PX // 8))
    FONT_SMALL = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        max(6, CARD_W_PX // 11))
except Exception:
    FONT_BIG = FONT_SMALL = ImageFont.load_default()


def make_front_card(raw_img: Image.Image | None, name_es: str) -> Image.Image:
    """Compose a single front card: photo centred on cream background."""
    card = Image.new("RGBA", (CARD_W_PX, CARD_H_PX), CARD_BG)
    draw = ImageDraw.Draw(card)

    # Reserve bottom strip for name label
    label_h = max(14, CARD_H_PX // 7)
    photo_area_h = CARD_H_PX - label_h - 4

    if raw_img is not None:
        # Fit image into photo area with padding
        pad = max(3, CARD_W_PX // 20)
        max_w = CARD_W_PX - 2 * pad
        max_h = photo_area_h - 2 * pad

        img = raw_img.convert("RGBA").copy()
        img.thumbnail((max_w, max_h), Image.LANCZOS)

        # Centre horizontally, place at top with pad
        x = (CARD_W_PX - img.width) // 2
        y = pad + (max_h - img.height) // 2
        card.paste(img, (x, y), img)
    else:
        # Placeholder: bug silhouette text
        bb = draw.textbbox((0, 0), "?", font=FONT_BIG)
        tw, th = bb[2]-bb[0], bb[3]-bb[1]
        draw.text(((CARD_W_PX-tw)//2, (photo_area_h-th)//2), "?",
                  fill=(190, 170, 130, 200), font=FONT_BIG)

    # Label background
    lx, ly = 0, CARD_H_PX - label_h
    draw.rectangle([lx, ly, CARD_W_PX, CARD_H_PX],
                   fill=(240, 228, 195, 255))

    # Name text  (truncate if too wide)
    bb = draw.textbbox((0, 0), name_es, font=FONT_SMALL)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    while tw > CARD_W_PX - 4 and len(name_es) > 3:
        name_es = name_es[:-2] + "."
        bb = draw.textbbox((0, 0), name_es, font=FONT_SMALL)
        tw, th = bb[2]-bb[0], bb[3]-bb[1]
    draw.text(((CARD_W_PX-tw)//2, ly + (label_h-th)//2),
              name_es, fill=TEXT_COL[:3], font=FONT_SMALL)

    # Outer border
    bw = max(1, CARD_W_PX // 60)
    draw.rectangle([bw//2, bw//2, CARD_W_PX-bw//2-1, CARD_H_PX-bw//2-1],
                   outline=BORDER_COL[:3], width=bw)

    return card


def make_back_card() -> Image.Image:
    """Draw the Bug Hunter back design."""
    BACK_BG    = (248, 244, 228, 255)
    DARK_GREEN = (45, 80, 45)
    MID_GREEN  = (100, 150, 80)
    LIGHT_GREEN= (180, 210, 150)

    card = Image.new("RGBA", (CARD_W_PX, CARD_H_PX), BACK_BG)
    draw = ImageDraw.Draw(card)

    # ---- subtle botanical background tiles ----
    leaf_pts = [
        (0.12, 0.12), (0.88, 0.12), (0.12, 0.88), (0.88, 0.88),
        (0.50, 0.08), (0.08, 0.50), (0.92, 0.50), (0.50, 0.92),
        (0.30, 0.30), (0.70, 0.30), (0.30, 0.70), (0.70, 0.70),
        (0.50, 0.50),
    ]
    lw_px = max(5, CARD_W_PX // 7)
    lh_px = max(8, CARD_H_PX // 5)
    for (rx, ry) in leaf_pts:
        cx = int(rx * CARD_W_PX)
        cy = int(ry * CARD_H_PX)
        draw.ellipse([cx-lw_px//2, cy-lh_px//2, cx+lw_px//2, cy+lh_px//2],
                     fill=(*LIGHT_GREEN, 110))
        # central vein
        draw.line([(cx, cy - lh_px//2), (cx, cy + lh_px//2)],
                  fill=(*MID_GREEN, 150), width=max(1, CARD_W_PX // 70))

    # ---- small decorative dots ----
    for dx, dy in [(0.22, 0.18), (0.78, 0.18), (0.22, 0.82), (0.78, 0.82)]:
        rx = int(dx * CARD_W_PX)
        ry = int(dy * CARD_H_PX)
        r = max(2, CARD_W_PX // 25)
        draw.ellipse([rx-r, ry-r, rx+r, ry+r], fill=(*MID_GREEN, 160))

    # ---- central medallion ----
    mcx, mcy = CARD_W_PX // 2, CARD_H_PX // 2
    outer_r = int(min(CARD_W_PX, CARD_H_PX) * 0.32)
    inner_r = int(outer_r * 0.82)

    draw.ellipse([mcx-outer_r, mcy-outer_r, mcx+outer_r, mcy+outer_r],
                 fill=(235, 248, 220, 255), outline=DARK_GREEN,
                 width=max(1, CARD_W_PX // 55))
    draw.ellipse([mcx-inner_r, mcy-inner_r, mcx+inner_r, mcy+inner_r],
                 outline=MID_GREEN, width=max(1, CARD_W_PX // 80))

    # ---- magnifying glass ----
    mg_r = int(outer_r * 0.38)
    mg_cy = int(mcy - outer_r * 0.08)
    draw.ellipse([mcx-mg_r, mg_cy-mg_r, mcx+mg_r, mg_cy+mg_r],
                 outline=DARK_GREEN, width=max(1, CARD_W_PX // 65))
    hlen = int(mg_r * 0.65)
    hx1 = int(mcx + mg_r * 0.70)
    hy1 = int(mg_cy + mg_r * 0.70)
    draw.line([(hx1, hy1), (hx1+hlen, hy1+hlen)],
              fill=DARK_GREEN, width=max(2, CARD_W_PX // 40))

    # ---- text  (BUG  HUNTER) ----
    try:
        f_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            max(6, int(CARD_W_PX * 0.13)))
    except Exception:
        f_title = ImageFont.load_default()

    for txt, dy_frac in [("BUG", -0.32), ("HUNTER", 0.10)]:
        bb = draw.textbbox((0, 0), txt, font=f_title)
        tw, th = bb[2]-bb[0], bb[3]-bb[1]
        ty = int(mcy + dy_frac * outer_r) - th // 2
        draw.text((mcx - tw//2, ty), txt, fill=DARK_GREEN, font=f_title)

    # ---- outer border ----
    bw = max(1, CARD_W_PX // 50)
    draw.rectangle([bw//2, bw//2, CARD_W_PX-bw//2-1, CARD_H_PX-bw//2-1],
                   outline=DARK_GREEN, width=bw)

    return card

# ---------------------------------------------------------------------------
# 5.  Download all insect images
# ---------------------------------------------------------------------------
print(f"\nDownloading {len(INSECTS)} insect images …")
raw_images: dict[str, Image.Image | None] = {}
for name_es, sci in INSECTS:
    raw_images[sci] = load_insect(name_es, sci)

ok = sum(1 for v in raw_images.values() if v is not None)
print(f"\n{ok}/{len(INSECTS)} images downloaded successfully.")

# ---------------------------------------------------------------------------
# 6.  Prepare all 72 front cards  + 1 shared back card
# ---------------------------------------------------------------------------
print("\nComposing cards …")
front_cards: list[tuple[str, Image.Image]] = []
for name_es, sci in INSECTS:
    card = make_front_card(raw_images[sci], name_es)
    front_cards.append((name_es, card))
    front_cards.append((name_es, card))   # duplicate = pair

back_card_img = make_back_card()

# ---------------------------------------------------------------------------
# 7.  Render a page of cards onto a ReportLab PDF canvas
# ---------------------------------------------------------------------------
def pt(mm_val): return mm_val * 72.0 / 25.4

PW_PT, PH_PT = A4
CW_PT = pt(CARD_W_MM)
CH_PT = pt(CARD_H_MM)
MG_PT = pt(MARGIN_MM)
GP_PT = pt(GAP_MM)


def render_page(c: rl_canvas.Canvas,
                cards: list[tuple[str, Image.Image]],
                cols: int, rows: int,
                mirror_cols: bool = False):
    """
    Draw cards grid on current PDF page.
    mirror_cols=True → column order is reversed for duplex long-edge alignment.
    """
    for slot_idx in range(cols * rows):
        row_i = slot_idx // cols
        col_i = slot_idx % cols

        if mirror_cols:
            col_i = cols - 1 - col_i
        card_idx = row_i * cols + col_i if not mirror_cols else row_i * cols + (cols-1-col_i)
        # Correct index for mirrored layout
        if mirror_cols:
            card_idx = slot_idx   # physical slot index (already accounting for draw order)

        if slot_idx >= len(cards):
            continue

        _, card_img = cards[slot_idx] if not mirror_cols else cards[slot_idx]

        # For mirrored: we fill slots left-to-right but draw at mirrored column
        draw_col = (cols - 1 - (slot_idx % cols)) if mirror_cols else (slot_idx % cols)
        draw_row = slot_idx // cols

        x_pt = MG_PT + draw_col * (CW_PT + GP_PT)
        # PDF y=0 is bottom; top of row 0 is at PH_PT - MG_PT
        y_pt = PH_PT - MG_PT - (draw_row + 1) * CH_PT - draw_row * GP_PT

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
            tmp = tf.name
        card_img.convert("RGB").save(tmp, "PNG", dpi=(TARGET_DPI, TARGET_DPI))
        c.drawImage(tmp, x_pt, y_pt, width=CW_PT, height=CH_PT,
                    preserveAspectRatio=False)
        os.unlink(tmp)

    # Dashed cut guides
    c.setStrokeColorRGB(0.65, 0.65, 0.65)
    c.setLineWidth(0.25)
    c.setDash([2, 5], 0)

    # Vertical guides
    for ci in range(cols + 1):
        if ci == 0:
            xg = MG_PT
        elif ci == cols:
            xg = MG_PT + cols * CW_PT + (cols - 1) * GP_PT
        else:
            xg = MG_PT + ci * (CW_PT + GP_PT) - GP_PT / 2
        c.line(xg, MG_PT, xg, PH_PT - MG_PT)

    # Horizontal guides
    for ri in range(rows + 1):
        if ri == 0:
            yg = PH_PT - MG_PT
        elif ri == rows:
            yg = MG_PT
        else:
            yg = PH_PT - MG_PT - ri * (CH_PT + GP_PT) + GP_PT / 2
        c.line(MG_PT, yg, PW_PT - MG_PT, yg)

    c.setDash([], 0)

# ---------------------------------------------------------------------------
# 8.  Write PDF
# ---------------------------------------------------------------------------
print(f"\nBuilding PDF → {OUTPUT_PATH}")
c = rl_canvas.Canvas(OUTPUT_PATH, pagesize=A4)
c.setTitle("Memotest Bug Hunter")
c.setAuthor("Bug Hunter Memotest Generator")

# Page 1 – Fronts
print("  Page 1: fronts …")
render_page(c, front_cards, COLS, ROWS, mirror_cols=False)
c.showPage()

# Page 2 – Backs (duplicate the single back design for all 72 slots)
print("  Page 2: backs …")
back_list = [("back", back_card_img)] * (COLS * ROWS)
render_page(c, back_list, COLS, ROWS, mirror_cols=True)
c.showPage()

c.save()

print(f"\n✓  Done!  →  {OUTPUT_PATH}")
print(f"   Grid: {COLS} cols × {ROWS} rows  "
      f"|  Card size: {CARD_W_MM:.1f} × {CARD_H_MM:.1f} mm  "
      f"|  Total cards: {TOTAL_CARDS} ({len(INSECTS)} unique bugs × 2)")
print(f"   Print DUPLEX on A4, flip on LONG edge (portrait), then cut on dashed lines.")
