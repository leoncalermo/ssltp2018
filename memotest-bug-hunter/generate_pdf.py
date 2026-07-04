#!/usr/bin/env python3
"""
Memotest Bug Hunter – PDF Generator  v2 (Watercolor Illustrations)
====================================================================
Generates a print-ready 2-page A4 PDF:
  Page 1 – all card fronts (AI watercolor illustrations, 36 unique bugs × 2 = 72 cards)
  Page 2 – all card backs  (uniform Bug Hunter botanical pattern, same grid)

Card design matches the original AI-art memotest style:
  • Cream/parchment background
  • Thin stitched dotted border
  • Watercolor bug illustration centred
  • Small magnifying-glass + branch logo in bottom-right corner
  • No text on card face

Optimised for duplex (long-edge flip) printing: cut on dashed guide lines.
"""

import os, math, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as rl_canvas

# ---------------------------------------------------------------------------
# 0.  Paths & config
# ---------------------------------------------------------------------------
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
ILLUS_DIR  = os.path.join(BASE_DIR, "illustrations")
OUTPUT     = os.path.join(BASE_DIR, "memotest_bug_hunter.pdf")

MARGIN_MM  = 6.0
GAP_MM     = 1.5
TARGET_DPI = 300

# ---------------------------------------------------------------------------
# 1.  Insect list  (filename_stem, spanish_name)
#     36 unique bugs → 72 cards (each appears exactly twice)
# ---------------------------------------------------------------------------
INSECTS = [
    ("bug_01_vaquita",          "Vaquita"),
    ("bug_02_abeja",            "Abeja miel"),
    ("bug_03_mariposa_monarca", "Mariposa monarca"),
    ("bug_04_mariposa_azul",    "Mariposa azul"),
    ("bug_05_saltamontes",      "Saltamontes"),
    ("bug_06_escarabajo_ciervo","Escarabajo ciervo"),
    ("bug_07_chinche_verde",    "Chinche verde"),
    ("bug_08_hormiga",          "Hormiga colorada"),
    ("bug_09_escarabajo_tierra","Escarabajo tierra"),
    ("bug_10_hormiga_negra",    "Hormiga negra"),
    ("bug_11_libelula_roja",    "Libélula roja"),
    ("bug_12_mantis",           "Mantis religiosa"),
    ("bug_13_abejorro",         "Abejorro"),
    ("bug_14_oruga",            "Oruga"),
    ("bug_15_mosca_azul",       "Mosca azul"),
    ("bug_16_libelula_azul",    "Libélula azul"),
    ("bug_17_escarabajo_rojo",  "Escarabajo rojo"),
    ("bug_18_abeja_solitaria",  "Abeja solitaria"),
    ("bug_19_langosta",         "Langosta"),
    ("bug_20_caracol",          "Caracol"),
    ("bug_21_insecto_palo",     "Insecto palo"),
    ("bug_22_chinche_grande",   "Chinche grande"),
    ("bug_23_luciernaga",       "Luciérnaga"),
    ("bug_24_lombriz",          "Lombriz"),
    ("bug_25_arana",            "Araña jardín"),
    ("bug_26_cochinilla",       "Cochinilla"),
    ("bug_27_escarabajo_negro", "Escarabajo negro"),
    ("bug_28_polilla",          "Polilla"),
    ("bug_29_ciempies",         "Ciempiés"),
    ("bug_30_mosca",            "Mosca doméstica"),
    ("bug_31_escorpion",        "Escorpión"),
    ("bug_32_langosta_marron",  "Langosta marrón"),
    ("bug_33_chinche_fuego",    "Chinche fuego"),
    ("bug_34_avispa",           "Avispa"),
    ("bug_35_babosa",           "Babosa"),
    ("bug_36_grillo",           "Grillo"),
]

assert len(INSECTS) == 36
TOTAL_CARDS = 72

# ---------------------------------------------------------------------------
# 2.  Optimal grid  (maximise card area for 72 cards on A4)
# ---------------------------------------------------------------------------
A4_W_MM, A4_H_MM = 210.0, 297.0

def best_grid(n, pw, ph, mg, gap):
    best, best_area = None, 0
    for cols in range(1, n + 1):
        rows = math.ceil(n / cols)
        cw = (pw - 2*mg - (cols-1)*gap) / cols
        ch = (ph - 2*mg - (rows-1)*gap) / rows
        if cw <= 0 or ch <= 0:
            continue
        if cw * ch > best_area:
            best_area = cw * ch
            best = (cols, rows, cw, ch)
    return best

COLS, ROWS, CARD_W_MM, CARD_H_MM = best_grid(
    TOTAL_CARDS, A4_W_MM, A4_H_MM, MARGIN_MM, GAP_MM)

def mm2px(x): return int(round(x / 25.4 * TARGET_DPI))
def mm2pt(x): return x * 72.0 / 25.4

CARD_W_PX = mm2px(CARD_W_MM)
CARD_H_PX = mm2px(CARD_H_MM)

print(f"Grid: {COLS}×{ROWS}  |  card: {CARD_W_MM:.2f}×{CARD_H_MM:.2f} mm  "
      f"| px: {CARD_W_PX}×{CARD_H_PX}")

# ---------------------------------------------------------------------------
# 3.  Card design constants
# ---------------------------------------------------------------------------
CARD_BG      = (250, 247, 237)   # warm cream parchment
BORDER_COL   = (185, 170, 140)   # tan border
DOT_COL      = (165, 148, 118)   # slightly darker dots for stitched effect
LOGO_COL     = (130, 155, 110)   # muted green for logo

PAD_RATIO    = 0.10              # padding around bug illustration (fraction of card size)

# ---------------------------------------------------------------------------
# 4.  Draw the logo (magnifying glass + small branch)  –  bottom-right corner
# ---------------------------------------------------------------------------
def draw_logo(draw: ImageDraw.ImageDraw, card_w: int, card_h: int):
    """Draw a small magnifying glass + olive branch in the bottom-right corner."""
    logo_size = max(12, int(min(card_w, card_h) * 0.13))
    margin    = int(logo_size * 0.55)
    cx = card_w - margin - logo_size // 2
    cy = card_h - margin - logo_size // 2

    lw = max(1, logo_size // 16)
    r  = int(logo_size * 0.35)

    # Magnifying glass circle
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 outline=LOGO_COL, width=max(1, lw))

    # Handle
    hlen = int(r * 0.85)
    angle_off = int(r * 0.70)
    draw.line([(cx + angle_off, cy + angle_off),
               (cx + angle_off + hlen, cy + angle_off + hlen)],
              fill=LOGO_COL, width=max(1, lw + 1))

    # Small olive/wheat branch on the right side of the glass
    bx = cx + r + 3
    by = cy - 2
    stem_len = int(logo_size * 0.40)
    draw.line([(bx, by + stem_len), (bx, by - stem_len)],
              fill=LOGO_COL, width=max(1, lw))
    leaf_h = int(stem_len * 0.30)
    leaf_w = int(stem_len * 0.40)
    for fy in [by - stem_len//3, by, by + stem_len//3]:
        # left leaf
        draw.ellipse([bx - leaf_w, fy - leaf_h // 2,
                      bx, fy + leaf_h // 2], fill=LOGO_COL)


# ---------------------------------------------------------------------------
# 5.  Compose a single front card
# ---------------------------------------------------------------------------
def make_front_card(illus_path: str) -> Image.Image:
    """
    Compose a front card:
      – cream parchment background
      – thin stitched/dotted border (two thin lines + dots)
      – bug illustration centred
      – magnifying-glass + branch logo bottom-right
    """
    card = Image.new("RGB", (CARD_W_PX, CARD_H_PX), CARD_BG)
    draw = ImageDraw.Draw(card)

    # ---- stitched border ----
    # Inner thin rectangle
    bpad = max(3, CARD_W_PX // 22)
    bw   = max(1, CARD_W_PX // 90)
    draw.rectangle([bpad, bpad, CARD_W_PX - bpad - 1, CARD_H_PX - bpad - 1],
                   outline=BORDER_COL, width=bw)

    # Dotted line just inside
    dot_pad  = bpad + bw + max(2, CARD_W_PX // 70)
    dot_gap  = max(4, CARD_W_PX // 28)
    dot_r    = max(1, CARD_W_PX // 110)

    def draw_dotted_line(x0, y0, x1, y1):
        steps = max(abs(x1-x0), abs(y1-y0))
        n     = max(1, steps // dot_gap)
        for i in range(n + 1):
            t  = i / max(1, n)
            dx = int(x0 + (x1-x0)*t)
            dy = int(y0 + (y1-y0)*t)
            draw.ellipse([dx-dot_r, dy-dot_r, dx+dot_r, dy+dot_r], fill=DOT_COL)

    draw_dotted_line(dot_pad, dot_pad, CARD_W_PX-dot_pad, dot_pad)          # top
    draw_dotted_line(CARD_W_PX-dot_pad, dot_pad, CARD_W_PX-dot_pad, CARD_H_PX-dot_pad)  # right
    draw_dotted_line(CARD_W_PX-dot_pad, CARD_H_PX-dot_pad, dot_pad, CARD_H_PX-dot_pad)  # bottom
    draw_dotted_line(dot_pad, CARD_H_PX-dot_pad, dot_pad, dot_pad)          # left

    # ---- bug illustration ----
    if os.path.exists(illus_path):
        raw = Image.open(illus_path).convert("RGBA")

        # Available area for the illustration
        pad  = int(CARD_W_PX * PAD_RATIO) + bpad + bw + 2
        avw  = CARD_W_PX - 2 * pad
        avh  = CARD_H_PX - 2 * pad

        raw.thumbnail((avw, avh), Image.LANCZOS)

        # White matte for the illustration (soften edges on cream bg)
        matte = Image.new("RGBA", raw.size, CARD_BG + (255,))
        combined = Image.alpha_composite(matte, raw).convert("RGB")

        x = pad + (avw - combined.width)  // 2
        y = pad + (avh - combined.height) // 2
        card.paste(combined, (x, y))

    # ---- logo ----
    draw_logo(draw, CARD_W_PX, CARD_H_PX)

    return card


# ---------------------------------------------------------------------------
# 6.  Compose back card  (Bug Hunter botanical pattern)
# ---------------------------------------------------------------------------
def make_back_card() -> Image.Image:
    BACK_BG      = (248, 244, 228)
    DARK_GREEN   = (45,  80,  45)
    MID_GREEN    = (95, 145,  75)
    LIGHT_GREEN  = (175, 210, 145)
    TEXT_GREEN   = (38,  68,  38)

    card = Image.new("RGB", (CARD_W_PX, CARD_H_PX), BACK_BG)
    draw = ImageDraw.Draw(card)

    # ---- botanical background: draw all leaves into one RGBA overlay ----
    overlay = Image.new("RGBA", (CARD_W_PX, CARD_H_PX), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    leaf_defs = [
        # (rx, ry, angle_deg)   angle: 0=vertical, 45=diagonal, 90=horizontal
        (0.08, 0.12, 30), (0.92, 0.12, -30),
        (0.08, 0.88, -30), (0.92, 0.88, 30),
        (0.50, 0.06,  0), (0.50, 0.94,  0),
        (0.06, 0.50, 90), (0.94, 0.50, 90),
        (0.25, 0.30, 45), (0.75, 0.30,-45),
        (0.25, 0.70,-45), (0.75, 0.70, 45),
    ]
    lw_px = max(6, CARD_W_PX // 7)
    lh_px = max(10, CARD_H_PX // 4)
    for rx, ry, ang in leaf_defs:
        lx, ly = int(rx * CARD_W_PX), int(ry * CARD_H_PX)
        # Draw leaf as a rotated ellipse using a small rotated sub-image
        leaf_sub = Image.new("RGBA", (lw_px*2+4, lh_px*2+4), (0, 0, 0, 0))
        ls = ImageDraw.Draw(leaf_sub)
        ls.ellipse([2, 2, lw_px*2+2, lh_px*2+2], fill=(*LIGHT_GREEN, 110))
        ls.line([(lw_px+2, 2), (lw_px+2, lh_px*2+2)],
                fill=(*MID_GREEN, 140), width=max(1, CARD_W_PX // 80))
        leaf_rot = leaf_sub.rotate(-ang, expand=True)
        ox = lx - leaf_rot.width // 2
        oy = ly - leaf_rot.height // 2
        overlay.paste(leaf_rot, (ox, oy), leaf_rot)

    card = Image.alpha_composite(card.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(card)

    # Small berries
    for rx, ry in [(0.18, 0.18), (0.82, 0.18), (0.18, 0.82), (0.82, 0.82)]:
        dx, dy = int(rx * CARD_W_PX), int(ry * CARD_H_PX)
        dr = max(2, CARD_W_PX // 32)
        draw.ellipse([dx-dr, dy-dr, dx+dr, dy+dr], fill=MID_GREEN)

    # ---- central medallion ----
    mcx, mcy = CARD_W_PX // 2, CARD_H_PX // 2
    out_r  = int(min(CARD_W_PX, CARD_H_PX) * 0.30)
    in_r   = int(out_r * 0.80)
    bw_med = max(1, CARD_W_PX // 55)

    # Fill
    draw.ellipse([mcx-out_r, mcy-out_r, mcx+out_r, mcy+out_r],
                 fill=(238, 248, 225))
    # Outer ring
    draw.ellipse([mcx-out_r, mcy-out_r, mcx+out_r, mcy+out_r],
                 outline=DARK_GREEN, width=bw_med)
    # Inner ring
    draw.ellipse([mcx-in_r, mcy-in_r, mcx+in_r, mcy+in_r],
                 outline=MID_GREEN, width=max(1, bw_med-1))

    # ---- magnifying glass inside medallion ----
    mg_r  = int(out_r * 0.36)
    mg_cy = int(mcy - out_r * 0.07)
    draw.ellipse([mcx-mg_r, mg_cy-mg_r, mcx+mg_r, mg_cy+mg_r],
                 outline=DARK_GREEN, width=max(1, CARD_W_PX // 65))
    hlen = int(mg_r * 0.68)
    hx1 = int(mcx + mg_r * 0.70)
    hy1 = int(mg_cy + mg_r * 0.70)
    draw.line([(hx1, hy1), (hx1+hlen, hy1+hlen)],
              fill=DARK_GREEN, width=max(2, CARD_W_PX // 42))

    # ---- text ----
    try:
        ft = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            max(7, int(CARD_W_PX * 0.12)))
    except Exception:
        ft = ImageFont.load_default()

    for txt, dy_frac in [("BUG", -0.34), ("HUNTER", 0.10)]:
        bb = draw.textbbox((0, 0), txt, font=ft)
        tw, th = bb[2]-bb[0], bb[3]-bb[1]
        ty = int(mcy + dy_frac * out_r) - th // 2
        draw.text((mcx - tw//2, ty), txt, fill=TEXT_GREEN, font=ft)

    # ---- card border (same stitched style as fronts) ----
    bpad2 = max(3, CARD_W_PX // 22)
    bw2   = max(1, CARD_W_PX // 90)
    draw.rectangle([bpad2, bpad2, CARD_W_PX-bpad2-1, CARD_H_PX-bpad2-1],
                   outline=DARK_GREEN, width=bw2)
    dot_pad2 = bpad2 + bw2 + max(2, CARD_W_PX // 70)
    dot_gap2 = max(4, CARD_W_PX // 28)
    dot_r2   = max(1, CARD_W_PX // 110)

    def draw_dotted2(x0, y0, x1, y1):
        steps = max(abs(x1-x0), abs(y1-y0))
        n     = max(1, steps // dot_gap2)
        for i in range(n+1):
            t  = i / max(1, n)
            dx = int(x0 + (x1-x0)*t)
            dy = int(y0 + (y1-y0)*t)
            draw.ellipse([dx-dot_r2, dy-dot_r2, dx+dot_r2, dy+dot_r2], fill=DARK_GREEN)

    draw_dotted2(dot_pad2, dot_pad2, CARD_W_PX-dot_pad2, dot_pad2)
    draw_dotted2(CARD_W_PX-dot_pad2, dot_pad2, CARD_W_PX-dot_pad2, CARD_H_PX-dot_pad2)
    draw_dotted2(CARD_W_PX-dot_pad2, CARD_H_PX-dot_pad2, dot_pad2, CARD_H_PX-dot_pad2)
    draw_dotted2(dot_pad2, CARD_H_PX-dot_pad2, dot_pad2, dot_pad2)

    return card


# ---------------------------------------------------------------------------
# 7.  Build all card images
# ---------------------------------------------------------------------------
print("\nComposing front cards …")
front_cards: list[Image.Image] = []
for stem, name in INSECTS:
    path = os.path.join(ILLUS_DIR, stem + ".png")
    card = make_front_card(path)
    front_cards.append(card)
    front_cards.append(card)   # pair → duplicate

print("Composing back card …")
back_card = make_back_card()

# ---------------------------------------------------------------------------
# 8.  Render page onto PDF canvas
# ---------------------------------------------------------------------------
PW_PT, PH_PT = A4
CW_PT = mm2pt(CARD_W_MM)
CH_PT = mm2pt(CARD_H_MM)
MG_PT = mm2pt(MARGIN_MM)
GP_PT = mm2pt(GAP_MM)


def render_page(c: rl_canvas.Canvas,
                cards: list[Image.Image],
                cols: int, rows: int,
                mirror_cols: bool = False):
    for slot in range(cols * rows):
        if slot >= len(cards):
            continue
        r_i = slot // cols
        c_i = slot %  cols
        draw_col = (cols - 1 - c_i) if mirror_cols else c_i

        x_pt = MG_PT + draw_col * (CW_PT + GP_PT)
        y_pt = PH_PT - MG_PT - (r_i + 1) * CH_PT - r_i * GP_PT

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
            tmp = tf.name
        cards[slot].save(tmp, "PNG", dpi=(TARGET_DPI, TARGET_DPI))
        c.drawImage(tmp, x_pt, y_pt, width=CW_PT, height=CH_PT,
                    preserveAspectRatio=False)
        os.unlink(tmp)

    # Dashed cut guides
    c.setStrokeColorRGB(0.60, 0.60, 0.60)
    c.setLineWidth(0.25)
    c.setDash([2, 5], 0)
    for ci in range(cols + 1):
        if ci == 0:         xg = MG_PT
        elif ci == cols:    xg = MG_PT + cols * CW_PT + (cols-1) * GP_PT
        else:               xg = MG_PT + ci * (CW_PT + GP_PT) - GP_PT / 2
        c.line(xg, MG_PT, xg, PH_PT - MG_PT)
    for ri in range(rows + 1):
        if ri == 0:         yg = PH_PT - MG_PT
        elif ri == rows:    yg = MG_PT
        else:               yg = PH_PT - MG_PT - ri * (CH_PT + GP_PT) + GP_PT / 2
        c.line(MG_PT, yg, PW_PT - MG_PT, yg)
    c.setDash([], 0)


# ---------------------------------------------------------------------------
# 9.  Write PDF
# ---------------------------------------------------------------------------
print(f"\nWriting PDF → {OUTPUT}")
c = rl_canvas.Canvas(OUTPUT, pagesize=A4)
c.setTitle("Memotest Bug Hunter")

print("  Page 1: fronts …")
render_page(c, front_cards, COLS, ROWS, mirror_cols=False)
c.showPage()

print("  Page 2: backs …")
back_list = [back_card] * (COLS * ROWS)
render_page(c, back_list, COLS, ROWS, mirror_cols=True)
c.showPage()

c.save()

print(f"\n✓  Done!  {OUTPUT}")
print(f"   Grid: {COLS}×{ROWS}  |  Card: {CARD_W_MM:.1f}×{CARD_H_MM:.1f} mm  "
      f"|  {TOTAL_CARDS} cards ({len(INSECTS)} unique × 2)")
print("   Print DUPLEX, flip on LONG EDGE (portrait). Cut on dashed lines.")
