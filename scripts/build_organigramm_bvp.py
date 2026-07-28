# -*- coding: utf-8 -*-
"""
Raeumt das Organigramm "Betriebs- und Verkehrsplanung" auf.

Vorgehen: die vorhandenen Platzhalter-Formen werden NICHT ersetzt, sondern
nur neu positioniert und in der Textformatierung vereinheitlicht. Dadurch
bleiben Fuellfarben, Schriften und Aufzaehlungszeichen exakt so, wie sie das
Master-Layout vorgibt - es aendert sich nur Geometrie und Auszeichnung.

Aenderungen:
  * alle fuenf Einheiten-Kaestchen exakt gleich breit
  * gleiche Hoehe je Ebene, Ebenen auf einem festen Raster
  * mittige Stammleitung, streng waagerechte Abzweige mit gleicher Laenge
  * Titelzeilen einheitlich fett ohne Unterstreichung
  * einheitlicher Zeilenabstand und Abstand Titel -> Namensliste
  * Tabelle: Kopfzeile, gleiche Zeilenhoehen, passende Spaltenbreiten
"""
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.enum.shapes import MSO_CONNECTOR
from pptx.enum.text import MSO_ANCHOR
from pptx.oxml.ns import qn
import copy

SRC = "organigramm/20250206_Organigramm_BVP_original.pptx"
DST = "organigramm/20250206_Organigramm_BVP_formatiert.pptx"

A = "http://schemas.openxmlformats.org/drawingml/2006/main"

# ---------------------------------------------------------------- Raster ----
SLIDE_W = 12192000
BAND_TOP, BAND_BOT = 1196752, 6309320     # grauer Inhaltsbereich aus dem Layout
MARGIN = 658813                            # Rand des Titel-Platzhalters uebernommen

TBL_W = 3850000
TBL_L = SLIDE_W - MARGIN - TBL_W           # 7683187
GUTTER = 600000                            # Abstand Diagramm <-> Tabelle

CHART_R = TBL_L - GUTTER                   # 7083187
CHART_L = MARGIN
W_BOX = 2800000                            # einheitliche Kaestchenbreite

BOX_L_LEFT = CHART_L                       # 658813
BOX_L_RIGHT = CHART_R - W_BOX              # 4283187
SPINE_X = (BOX_L_LEFT + W_BOX + BOX_L_RIGHT) // 2   # 3871000, exakt mittig

# Senkrechtes Raster
ROOT_T, ROOT_H = 1300000, 620000
T1, H_SMALL = 2080000, 700000              # Ebene 1: Projekt | Fachl. Support
VG = 260000                                # Abstand zwischen den Ebenen
T2 = T1 + H_SMALL + VG                     # 3040000  Ebene 2: Analyst
T3 = T2 + H_SMALL + VG                     # 4000000  Ebene 3: Bahn | Bus
H_BIG = 2050000
H_SPAN = 2 * H_SMALL + VG                  # 1555000  Fachl. Support ueber 2 Ebenen

BAR_Y = (ROOT_T + ROOT_H + T1) // 2        # 2020000

LINE_W = 19050                             # 1,5 pt (Original: 3 pt, sehr wuchtig)

# Kaestchen: id -> (left, top, width, height, Anzahl Titelabsaetze)
PLACE = {
    6:  (SPINE_X - W_BOX // 2, ROOT_T, W_BOX, ROOT_H, 2),   # LEITER (rot)
    14: (BOX_L_LEFT,  T1, W_BOX, H_SMALL, 1),               # Projekt- und Prozessmanagement
    42: (BOX_L_LEFT,  T2, W_BOX, H_SMALL, 1),               # Analyst Dienst-/Schichtplaene
    12: (BOX_L_RIGHT, T1, W_BOX, H_SPAN,  2),               # Fachl. Support und Administration
    20: (BOX_L_LEFT,  T3, W_BOX, H_BIG,   1),               # BVP Bahn
    33: (BOX_L_RIGHT, T3, W_BOX, H_BIG,   1),               # BVP Bus
}

# Texte, die im Original nur wegen der schmalen Kaestchen umbrochen waren
RETEXT = {
    14: ["Projekt- und Prozessmanagement"],          # war "Prozess-management"
    42: ["Analyst Dienst-/Schichtpläne"],            # war auf 2 Absaetze verteilt
}

CONNECT = [6, 14, 42, 12, 20, 33]
DROP_SHAPES = {37, 40, 26, 48}              # alte, schiefe Winkelverbinder

TBL_COLS = [1450000, 950000, 1450000]       # Nachname | Vorname | Umfang
TBL_HEAD = ["Nachname", "Vorname", "Umfang"]
TBL_T = ROOT_T
TBL_ROW_H = 197000

# ------------------------------------------------------------- Hilfsmittel --
def el(tag, **attrs):
    from lxml import etree
    e = etree.SubElement(etree.Element("{%s}dummy" % A), "{%s}%s" % (A, tag))
    for k, v in attrs.items():
        e.set(k, v)
    e.getparent().remove(e)
    return e


def paragraphs(tf):
    return tf._txBody.findall(qn("a:p"))


def has_run(p):
    return p.find(qn("a:r")) is not None


def set_run_attr(p, **attrs):
    """Attribute auf allen Runs eines Absatzes setzen bzw. entfernen (None)."""
    for r in p.findall(qn("a:r")):
        rPr = r.find(qn("a:rPr"))
        if rPr is None:
            rPr = el("rPr", lang="de-DE")
            r.insert(0, rPr)
        for k, v in attrs.items():
            if v is None:
                if k in rPr.attrib:
                    del rPr.attrib[k]
            else:
                rPr.set(k, v)


def bullet_pPr(p, space_before=None):
    """Absatz als Aufzaehlungspunkt formatieren - einheitlich fuer alle Namen."""
    old = p.find(qn("a:pPr"))
    if old is not None:
        p.remove(old)
    pPr = el("pPr", marL="171450", indent="-171450", algn="l")
    lnSpc = el("lnSpc")
    lnSpc.append(el("spcPct", val="100000"))
    pPr.append(lnSpc)
    spcBef = el("spcBef")
    # Absatzabstand: vor dem ersten Namen mehr Luft, danach keiner
    spcBef.append(el("spcPts", val=str(space_before if space_before else 0)))
    pPr.append(spcBef)
    pPr.append(el("buFont", typeface="Arial", pitchFamily="34", charset="0"))
    pPr.append(el("buChar", char="•"))
    p.insert(0, pPr)


def title_pPr(p):
    """Titelabsatz: zentriert, ohne Aufzaehlungszeichen, ohne Zusatzabstand."""
    old = p.find(qn("a:pPr"))
    if old is not None:
        p.remove(old)
    pPr = el("pPr", marL="0", indent="0", algn="ctr")
    lnSpc = el("lnSpc")
    lnSpc.append(el("spcPct", val="100000"))
    pPr.append(lnSpc)
    spcBef = el("spcBef")
    spcBef.append(el("spcPts", val="0"))
    pPr.append(spcBef)
    pPr.append(el("buNone"))
    p.insert(0, pPr)


def set_body(tf, anchor="t"):
    bodyPr = tf._txBody.find(qn("a:bodyPr"))
    for tag in ("a:normAutofit", "a:spAutoFit"):
        e = bodyPr.find(qn(tag))
        if e is not None:
            bodyPr.remove(e)
    bodyPr.set("anchor", anchor)
    bodyPr.set("lIns", "108000")
    bodyPr.set("rIns", "108000")
    bodyPr.set("tIns", "54000")
    bodyPr.set("bIns", "54000")
    bodyPr.append(el("noAutofit"))


def add_line(shapes, x1, y1, x2, y2, name):
    assert x1 == x2 or y1 == y2, "nur orthogonale Linien"
    cn = shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                              Emu(x1), Emu(y1), Emu(x2), Emu(y2))
    cn.name = name
    sp = cn._element
    st = sp.find(qn("p:style"))
    if st is not None:
        sp.remove(st)
    spPr = sp.find(qn("p:spPr"))
    ln = el("ln", w=str(LINE_W))
    fill = el("solidFill")
    clr = el("schemeClr", val="tx1")
    clr.append(el("lumMod", val="50000"))
    clr.append(el("lumOff", val="50000"))
    fill.append(clr)
    ln.append(fill)
    spPr.append(ln)
    cn.shadow.inherit = False
    return cn


# ------------------------------------------------------------------ Aufbau --
prs = Presentation(SRC)
slide = prs.slides[0]
shapes = slide.shapes
by_id = {sh.shape_id: sh for sh in shapes}

# --- 1. alte Winkelverbinder entfernen -------------------------------------
for sid in DROP_SHAPES:
    sh = by_id[sid]
    sh._element.getparent().remove(sh._element)

# --- 2. Kaestchen setzen und Text vereinheitlichen -------------------------
for sid, (L, T, W, H, n_title) in PLACE.items():
    sh = by_id[sid]
    sh.left, sh.top, sh.width, sh.height = Emu(L), Emu(T), Emu(W), Emu(H)
    tf = sh.text_frame
    set_body(tf, anchor="ctr" if sid == 6 else "t")

    # leere Absaetze raus - sie waren im Original der Ersatz fuer Absatzabstand
    for p in paragraphs(tf):
        if not has_run(p):
            tf._txBody.remove(p)

    ps = paragraphs(tf)

    # Titel, die nur wegen zu schmaler Kaestchen umbrochen waren, zusammenziehen
    if sid in RETEXT:
        new = RETEXT[sid]
        for i, txt in enumerate(new):
            ps[i].findall(qn("a:r"))[0].find(qn("a:t")).text = txt
            for extra in ps[i].findall(qn("a:r"))[1:]:
                ps[i].remove(extra)
        # ueberzaehlige alte Titelabsaetze entfernen
        old_titles = 2 if sid == 42 else 1
        for p in ps[len(new):old_titles]:
            tf._txBody.remove(p)
        ps = paragraphs(tf)

    for i, p in enumerate(ps):
        if i < n_title:
            title_pPr(p)
            # einheitlich fett, keine Unterstreichung (Bahn/Bus waren abweichend)
            set_run_attr(p, b="1", u=None)
        else:
            # 6 pt Luft nur vor dem ersten Namen, danach dichte Liste
            bullet_pPr(p, space_before=600 if i == n_title else 0)
            set_run_attr(p, b="0", u=None)

# Der rote LEITER-Kasten bekommt keine Aufzaehlung - beide Zeilen sind Titel
by_id[6].text_frame  # (bereits ueber n_title=2 abgedeckt)

# --- 3. Verbindungslinien neu ziehen ---------------------------------------
cy_projekt = T1 + H_SMALL // 2
cy_support = T1 + H_SPAN // 2
cy_analyst = T2 + H_SMALL // 2
cy_bottom = T3 + H_BIG // 2

# Stammleitung von der Leitung bis zur untersten Ebene
add_line(shapes, SPINE_X, ROOT_T + ROOT_H, SPINE_X, cy_bottom, "Stammleitung")

# Abzweige - alle exakt gleich lang (412187 EMU je Seite)
add_line(shapes, SPINE_X, cy_projekt, BOX_L_LEFT + W_BOX, cy_projekt,
         "Abzweig Projekt")
add_line(shapes, SPINE_X, cy_analyst, BOX_L_LEFT + W_BOX, cy_analyst,
         "Abzweig Analyst")
add_line(shapes, SPINE_X, cy_support, BOX_L_RIGHT, cy_support,
         "Abzweig Fachl. Support")
# unterste Ebene: eine durchgehende Waagerechte durch die Stammleitung
add_line(shapes, BOX_L_LEFT + W_BOX, cy_bottom, BOX_L_RIGHT, cy_bottom,
         "Abzweig Bahn/Bus")

# --- 4. Tabelle -------------------------------------------------------------
gf = [sh for sh in shapes if getattr(sh, "has_table", False) and sh.has_table][0]
tbl = gf.table
gf.left, gf.top = Emu(TBL_L), Emu(TBL_T)

for c, w in zip(tbl.columns, TBL_COLS):
    c.width = Emu(w)

tblEl = tbl._tbl
first_tr = tblEl.findall(qn("a:tr"))[0]

# Kopfzeile: Klon der ersten Datenzeile, damit Stil und Raender identisch sind
head = copy.deepcopy(first_tr)
# WICHTIG: Der Klon bringt die a16:rowId der Quellzeile mit. Doppelte IDs
# laesst PowerPoint nicht durch ("Datei kann nicht gelesen werden"), waehrend
# LibreOffice und die XSD-Pruefung sie klaglos akzeptieren. Die IDs sind reine
# Co-Authoring-Metadaten und duerfen ersatzlos entfallen.
for ext in head.findall(qn("a:extLst")):
    head.remove(ext)
for tc in head.findall(qn("a:tc")):
    for ext in tc.findall(qn("a:extLst")):
        tc.remove(ext)
for tc, label in zip(head.findall(qn("a:tc")), TBL_HEAD):
    for p in tc.findall(".//" + qn("a:p")):
        for r in p.findall(qn("a:r"))[1:]:
            p.remove(r)
        runs = p.findall(qn("a:r"))
        if runs:
            runs[0].find(qn("a:t")).text = label
            rPr = runs[0].find(qn("a:rPr"))
            rPr.set("b", "1")
            rPr.set("sz", "900")
            # Reste aus der geklonten Zelle (z. B. Rechtschreib-Flag) entfernen
            if "err" in rPr.attrib:
                del rPr.attrib["err"]
for tc in head.findall(qn("a:tc")):
    # Kopfzeile im selben Grau wie die Stabsstellen-Kaestchen, Text weiss -
    # verbindet Tabelle und Diagramm optisch, ohne neue Farben einzufuehren
    tcPr = tc.find(qn("a:tcPr"))
    fill = el("solidFill")
    clr = el("schemeClr", val="tx1")
    clr.append(el("lumMod", val="50000"))
    clr.append(el("lumOff", val="50000"))
    fill.append(clr)
    tcPr.append(fill)          # solidFill steht laut XSD hinter den ln*-Elementen
    for r in tc.findall(".//" + qn("a:r")):
        rPr = r.find(qn("a:rPr"))
        white = el("solidFill")
        white.append(el("schemeClr", val="bg1"))
        eff = rPr.find(qn("a:effectLst"))
        if eff is not None:
            eff.addprevious(white)   # Fuellung muss vor effectLst stehen
        else:
            rPr.append(white)
tblEl.insert(list(tblEl).index(first_tr), head)

# einheitliche Zeilenhoehen - im Original schwankten sie zwischen 181064 und 187397
for tr in tblEl.findall(qn("a:tr")):
    tr.set("h", str(TBL_ROW_H))

gf.height = Emu(TBL_ROW_H * len(tblEl.findall(qn("a:tr"))))

# --- 5. Fussnote ausrichten -------------------------------------------------
note = by_id[34]
note.left, note.top = Emu(CHART_L), Emu(T3 + H_BIG + 80000)

prs.save(DST)
print("gespeichert:", DST)
print("Spalten links/rechts:", BOX_L_LEFT, BOX_L_RIGHT, " Stamm x:", SPINE_X)
print("Abzweiglaenge:", SPINE_X - (BOX_L_LEFT + W_BOX), "/", BOX_L_RIGHT - SPINE_X)
print("Ebenen T1/T2/T3:", T1, T2, T3, " Unterkante:", T3 + H_BIG)
print("Tabelle:", TBL_L, TBL_T, sum(TBL_COLS), "Zeilen:", len(tblEl.findall(qn("a:tr"))))
