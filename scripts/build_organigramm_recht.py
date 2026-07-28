# -*- coding: utf-8 -*-
"""
Baut das Organigramm "Transdev Rechtsabteilung" geometrisch neu auf.

Ziel: alle Kaestchen exakt gleich gross, auf einem starren Raster
(5 Spalten x 6 Zeilen), alle Verbindungslinien exakt waagerecht bzw.
senkrecht, mit durchgaengig gleichen Abstaenden.

Inhalte (Texte, Farben, Kapitaelchen, Gelb-Markierung) werden 1:1
uebernommen; nur Position, Groesse und Schriftgroesse werden vereinheitlicht.
"""
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
import copy

SRC = "organigramm/20260727_Organigramm_Recht_original.pptx"
DST = "organigramm/20260727_Organigramm_Recht_formatiert.pptx"

# ---------------------------------------------------------------- Raster ----
SLIDE_W = 12192000
SLIDE_H = 6858000

# Grauer Inhaltsbereich kommt aus dem Layout: y = 1196752 .. 6309320
BAND_TOP = 1196752
BAND_BOT = 6309320

N_COLS = 6           # 5 Spalten
W_BOX = 1960000      # einheitliche Kaestchenbreite  (alle Kaestchen gleich)
H_BOX = 540000       # einheitliche Kaestchenhoehe   (alle Kaestchen gleich)
G_COL = 340000       # Spaltenabstand
M_SIDE = 516000      # Seitenrand: 2*516000 + 5*1960000 + 4*340000 = 12192000

V_GAP = 232000       # Zeilenabstand
PITCH = H_BOX + V_GAP            # 772000
R0 = 1290000                     # Oberkante Wurzelkaestchen

ARM = 170000         # Laenge der waagerechten Stichleitung zum Kaestchen
LINE_W = 9525        # 0,75 pt - wie im Original
CLR_LINE = "87A0B4"
CLR_BOX = "87A0B4"
CLR_ROOT = "FF0000"
CLR_TXT = "FFFFFF"
CLR_DARK = "000000"
CLR_MARK = "FFFF00"

FONT = "Arial"
FONT_ROOT = "Verdana"
SZ_BODY = 700        # 7,0 pt (Original: uneinheitlich 6,4 pt / 8,0 pt gemischt)
SZ_ROOT = 800        # 8,0 pt

# Spaltenmitten
CX = [M_SIDE + W_BOX // 2 + k * (W_BOX + G_COL) for k in range(5)]
# -> [1496000, 3796000, 6096000, 8396000, 10696000]  (Spalte 2 = Folienmitte)

# Zeilenoberkanten
RY = [R0 + r * PITCH for r in range(6)]
# -> [1290000, 2062000, 2834000, 3606000, 4378000, 5150000]

BOX_L = [cx - W_BOX // 2 for cx in CX]       # linke Kante je Spalte
TRUNK = [cx - W_BOX // 2 - ARM for cx in CX]  # x der senkrechten Sammelleitung

BAR_Y = (RY[0] + H_BOX + RY[1]) // 2          # waagerechter Verteilerbalken
ELBOW_Y = RY[1] + H_BOX + V_GAP // 2          # Knick, ab dem die Trunks laufen

def cy(row):
    """Senkrechte Mitte einer Rasterzeile."""
    return RY[row] + H_BOX // 2

# ---------------------------------------------------------------- Inhalte ---
# (Text, KAPITAELCHEN?, Markierung?)  - Reihenfolge = Zeilen im Kaestchen
ROOT_TXT = [("Leiterin Recht - Anja Kühler", False, False),
            ("(Stellvertreter - Adrian Hubig)", False, False)]

BOXES = [
    # --- Zeile 1: direkte Unterstellungen unter die Leiterin -----------------
    dict(key="A",  col=0, row=1, lines=[
        ("Kartell-, Regulierungs- und Vergaberecht *", True, False),
        ("Leitung: Adrian Hubig", False, False),
        ("1,0 FTE", False, False)]),
    dict(key="B",  col=1, row=1, lines=[
        ("Schadens- und Versicherungsrecht", True, False),
        ("Cornelia Sauer", False, False),
        ("0,6 FTE", False, False)]),
    dict(key="C",  col=2, row=1, lines=[
        ("Gesellschaftsrecht, M&A Beteiligungsverwaltung **", True, False),
        ("Leitung: Anja Kühler", False, False)]),
    dict(key="E",  col=4, row=1, lines=[
        ("Wirtschaftsrecht ***", True, False),
        ("Leitung: Sylvia Altrock", False, False),
        ("1,0 FTE", False, False)]),

    # --- Spalte A: Kartell-, Regulierungs- und Vergaberecht ------------------
    dict(key="A1", col=0, row=2, lines=[
        ("Kartell- und Regulierungsrecht", True, False),
        ("Einnahme-Aufteilung / Tarife", True, False),
        ("Adrian Hubig", False, False)]),
    dict(key="A2", col=0, row=3, lines=[
        ("Vergaberecht *", True, False),
        ("Lena Voigt", False, False),
        ("1,0 FTE", False, False),
        ("EZ", False, False)]),
    dict(key="A3", col=0, row=4, lines=[
        ("Vergaberecht *", True, False),
        ("Luisa Härtel", False, False),
        ("1,0 FTE", False, False)]),

    # --- Spalte C: Gesellschaftsrecht / M&A / Beteiligungsverwaltung ---------
    dict(key="C1", col=2, row=2, lines=[
        ("Gesellschaftsrecht / M&A", True, False),
        ("Anja Kühler + Adrian Hubig", False, False)]),
    dict(key="C2", col=2, row=3, lines=[
        ("Gesellschaftsrecht / Beteiligungsverwaltung **", True, False),
        ("Linda Hielscher", False, False),
        ("0,85 FTE", False, False)]),
    dict(key="C3", col=2, row=4, lines=[
        ("Gesellschaftsrecht Beteiligungsverwaltung **", True, False),
        ("Barbara Schilling", False, False),
        ("0,59 FTE", False, False)]),
    dict(key="C4", col=2, row=5, lines=[
        ("Trainee claim management", True, False),
        ("Maxi-Mercedes Jahn", False, False),
        ("1,0 FTE", False, False),
        ("ab 01.10.2026", False, True)]),

    # --- Spalte D: Arbeitsrecht (im Original ohne Kopf-Kaestchen) ------------
    dict(key="D1", col=3, row=2, lines=[
        ("Arbeitsrecht Bahngesellschaften + Holding, Führungsrkräfte", True, False),
        ("Jana Schulze", False, False)]),
    dict(key="D1a", col=3, row=3, lines=[
        ("Junior Legal Counsel", True, False),
        ("Jessica De Franco", False, False),
        ("1,0 FTE", False, False)]),
    dict(key="D2", col=3, row=4, lines=[
        ("Arbeitsrecht Busgesellschaften", True, False),
        ("Thorsten Röhrig", False, False)]),

    # --- Spalte E: Wirtschaftsrecht ------------------------------------------
    dict(key="E1", col=4, row=2, lines=[
        ("Wirtschaftsrecht Schienengesellschaften", True, False),
        ("Sylvia Altrock", False, False)]),
    dict(key="E2", col=4, row=3, lines=[
        ("Wirtschaftsrecht", True, False),
        ("Xenia Penz", False, False),
        ("0,5 FTE", False, False)]),
    dict(key="E3", col=4, row=4, lines=[
        ("Wirtschaftsrecht", True, False),
        ("David Scholten", False, False),
        ("1,0 FTE", False, False)]),
]

# ------------------------------------------------------------- Hilfsmittel --
def strip_style(shape):
    """Theme-Stil (Schatten/Akzentfarbe) entfernen - wir setzen alles explizit."""
    sp = shape._element
    st = sp.find(qn("p:style"))
    if st is not None:
        sp.remove(st)


def set_solid_fill(shape, hexcolor):
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor.from_string(hexcolor)


def set_line(shape, hexcolor=None, width=None):
    if hexcolor is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = RGBColor.from_string(hexcolor)
        shape.line.width = Emu(width)


def fill_textframe(shape, lines, size, font, bold=False,
                   color=CLR_TXT, line_spacing=0.92):
    """Textrahmen mit einheitlicher Formatierung neu aufbauen."""
    tf = shape.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Emu(36000)
    tf.margin_right = Emu(36000)
    tf.margin_top = Emu(18000)
    tf.margin_bottom = Emu(18000)
    # Autofit ausschalten - die Kaestchen sollen exakt gleich gross bleiben
    bodyPr = tf._txBody.find(qn("a:bodyPr"))
    for tag in ("a:normAutofit", "a:spAutoFit"):
        el = bodyPr.find(qn(tag))
        if el is not None:
            bodyPr.remove(el)
    bodyPr.append(bodyPr.makeelement(qn("a:noAutofit"), {}))

    for i, (text, caps, mark) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.CENTER
        p.line_spacing = line_spacing
        p.space_before = Pt(0)
        p.space_after = Pt(0)
        r = p.add_run()
        r.text = text
        rPr = r._r.get_or_add_rPr()
        rPr.set("sz", str(size))
        rPr.set("b", "1" if bold else "0")
        rPr.set("dirty", "0")
        if caps:
            rPr.set("cap", "all")
        # Farbe
        fill = rPr.makeelement(qn("a:solidFill"), {})
        clr = fill.makeelement(qn("a:srgbClr"),
                               {"val": CLR_DARK if mark else color})
        fill.append(clr)
        rPr.append(fill)
        # Gelbe Markierung (nur "ab 01.10.2026")
        if mark:
            hl = rPr.makeelement(qn("a:highlight"), {})
            hl.append(hl.makeelement(qn("a:srgbClr"), {"val": CLR_MARK}))
            rPr.append(hl)
        latin = rPr.makeelement(qn("a:latin"), {"typeface": font})
        rPr.append(latin)
        cs = rPr.makeelement(qn("a:cs"), {"typeface": font})
        rPr.append(cs)


def add_box(shapes, left, top, width, height, lines, name,
            fillc=CLR_BOX, size=SZ_BODY, font=FONT, bold=False):
    sh = shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(left), Emu(top),
                          Emu(width), Emu(height))
    sh.name = name
    strip_style(sh)
    set_solid_fill(sh, fillc)
    set_line(sh, None)          # randlos - einheitliche Optik
    sh.shadow.inherit = False
    fill_textframe(sh, lines, size, font, bold=bold)
    return sh


def add_line(shapes, x1, y1, x2, y2, name):
    """Streng waagerechte oder senkrechte Verbindungslinie."""
    assert x1 == x2 or y1 == y2, "nur orthogonale Linien"
    cn = shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                              Emu(x1), Emu(y1), Emu(x2), Emu(y2))
    cn.name = name
    strip_style(cn)
    cn.line.color.rgb = RGBColor.from_string(CLR_LINE)
    cn.line.width = Emu(LINE_W)
    cn.shadow.inherit = False
    return cn


# ------------------------------------------------------------------ Aufbau --
prs = Presentation(SRC)
slide = prs.slides[0]
spTree = slide.shapes._spTree

KEEP = {2, 3, 85, 45, 78}       # Titel, roter Marker, "Stand:", Hinweis, Fussnoten
for sh in list(slide.shapes):
    if sh.shape_id not in KEEP:
        sh._element.getparent().remove(sh._element)

shapes = slide.shapes

# --- 1. Verbindungslinien zuerst (liegen damit hinter den Kaestchen) --------
# Stamm von der Leiterin zum Verteilerbalken
add_line(shapes, CX[2], RY[0] + H_BOX, CX[2], BAR_Y, "Stamm Leitung")

# Waagerechter Verteilerbalken ueber alle 5 Spalten
add_line(shapes, CX[0], BAR_Y, CX[4], BAR_Y, "Verteilerbalken")

# Senkrechte Abgaenge vom Balken in die Kopf-Kaestchen (Spalten 0,1,2,4)
for c in (0, 1, 2, 4):
    add_line(shapes, CX[c], BAR_Y, CX[c], RY[1], "Abgang Spalte %d" % c)

# Spalte 3 (Arbeitsrecht) hat kein Kopf-Kaestchen:
# Abgang laeuft vom Balken durch die leere Zeile 1 bis zum Knickpunkt
add_line(shapes, CX[3], BAR_Y, CX[3], ELBOW_Y, "Abgang Spalte 3")

# Sammelleitungen ("Kaemme") je Spalte + waagerechte Stiche in die Kaestchen
COMB = {0: [2, 3, 4], 2: [2, 3, 4, 5], 3: [2, 4], 4: [2, 3, 4]}
for c, rows in COMB.items():
    tx = TRUNK[c]
    # Knick: von der Spaltenmitte waagerecht auf die Sammelleitung
    add_line(shapes, CX[c], ELBOW_Y, tx, ELBOW_Y, "Knick Spalte %d" % c)
    # Senkrechte Sammelleitung bis zur Mitte des untersten Kaestchens
    add_line(shapes, tx, ELBOW_Y, tx, cy(rows[-1]), "Sammelleitung Spalte %d" % c)
    # Waagerechte Stiche
    for r in rows:
        add_line(shapes, tx, cy(r), BOX_L[c], cy(r),
                 "Stich Spalte %d Zeile %d" % (c, r))

# Junior Legal Counsel haengt direkt unter "Arbeitsrecht Bahngesellschaften"
add_line(shapes, CX[3], RY[2] + H_BOX, CX[3], RY[3], "Stamm Junior Legal Counsel")

# --- 2. Kaestchen ----------------------------------------------------------
# Wurzel: gleiche Hoehe wie alle anderen, Breite = 2 Spalten (Kopf der Struktur)
root_w = 2 * W_BOX + G_COL
add_box(shapes, (SLIDE_W - root_w) // 2, RY[0], root_w, H_BOX,
        ROOT_TXT, "Leitung Recht", fillc=CLR_ROOT, size=SZ_ROOT,
        font=FONT_ROOT, bold=True)

for b in BOXES:
    add_box(shapes, BOX_L[b["col"]], RY[b["row"]], W_BOX, H_BOX,
            b["lines"], "Kasten %s" % b["key"])

# --- 3. Fussnoten / Hinweise sauber ausrichten ------------------------------
by_id = {sh.shape_id: sh for sh in slide.shapes}

fn = by_id[78]                    # Fussnoten * / ** / ***
fn.left, fn.top = Emu(7100000), Emu(5860000)
fn.width, fn.height = Emu(4576000), Emu(369332)

note = by_id[45]                  # "Das Organigramm ist nur fuer den internen..."
note.left, note.top = Emu(M_SIDE), Emu(5861000)   # 1. Zeile buendig mit Fussnote

stand = by_id[85]                 # "Stand: 10.07.2026"
stand.left = Emu(7100000)         # linksbuendig mit dem Fussnotenblock

prs.save(DST)
print("gespeichert:", DST)
print("Spaltenmitten :", CX)
print("Zeilenoberkanten:", RY)
print("Balken y =", BAR_Y, " Knick y =", ELBOW_Y)
print("Kasten: %d x %d EMU  (%.2f x %.2f Zoll)"
      % (W_BOX, H_BOX, W_BOX / 914400, H_BOX / 914400))
print("Unterkante Chart:", RY[5] + H_BOX, " / Band-Unterkante:", BAND_BOT)
