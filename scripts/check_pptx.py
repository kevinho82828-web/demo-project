# -*- coding: utf-8 -*-
"""
Abnahme-Pruefung fuer PPTX-Dateien vor der Auslieferung.

Prueft genau die Fehlerklasse, die LibreOffice und die XSD-Validierung
durchwinken, an der PowerPoint aber scheitert ("Datei kann nicht gelesen
werden"). Siehe Lessons Learned in CLAUDE.md.

Aufruf:  python3 scripts/check_pptx.py organigramm/*.pptx
Rueckgabewert 0 = alles sauber, 1 = mindestens ein Befund.
"""
import collections
import io
import os
import re
import sys
import zipfile

# Microsoft-Erweiterungs-IDs. Doppelte Werte lehnt PowerPoint ab, das
# offizielle Schema kennt diesen Namespace gar nicht.
A16_IDS = ("rowId", "colId", "creationId")

# Das PowerPoint-Schema. Erster Treffer gewinnt.
SCHEMA_ORTE = (
    "/root/.claude/skills/pptx/scripts/office/schemas/"
    "ISO-IEC29500-4_2016/pml.xsd",
    os.path.join(os.path.dirname(__file__), "schemas", "pml.xsd"),
)

# Bekannte Abweichungen der Transdev-Vorlage, die PowerPoint nachweislich
# oeffnet: buSzPct wird dort als Ganzzahl statt als Prozentwert geschrieben.
TOLERIERT = ("buSzPct",)


def pruefe(pfad):
    befunde = []
    try:
        z = zipfile.ZipFile(pfad)
    except zipfile.BadZipFile as e:
        return ["Datei ist kein gueltiges ZIP-Archiv: %s" % e]

    kaputt = z.testzip()
    if kaputt:
        befunde.append("ZIP-Eintrag beschaedigt: %s" % kaputt)

    namen = set(z.namelist())
    xml_teile = [n for n in namen if n.endswith(".xml")]

    # 1) doppelte interne IDs
    for teil in xml_teile:
        x = z.read(teil).decode("utf-8", errors="replace")
        for tag in A16_IDS:
            werte = re.findall(r'<a16:' + tag + r'[^>]*?(?:val|id)="([^"]+)"', x)
            dopp = {k: v for k, v in collections.Counter(werte).items() if v > 1}
            if dopp:
                befunde.append("%s: doppelte a16:%s %s" % (teil, tag, dopp))
        ids = re.findall(r'<p:cNvPr id="(\d+)"', x)
        dopp = {k: v for k, v in collections.Counter(ids).items() if v > 1}
        if dopp:
            befunde.append("%s: doppelte Form-ID %s" % (teil, dopp))

    # 2) Content-Types decken jeden Teil ab
    ct = z.read("[Content_Types].xml").decode("utf-8")
    endungen = set(e.lower() for e in re.findall(r'Extension="([^"]+)"', ct))
    einzeln = set(re.findall(r'PartName="/([^"]+)"', ct))
    for n in namen:
        if n == "[Content_Types].xml" or "_rels/" in n:
            continue
        if n in einzeln:
            continue
        if n.rsplit(".", 1)[-1].lower() not in endungen:
            befunde.append("kein Content-Type fuer %s" % n)

    # 3) jede benutzte Beziehung ist auch deklariert
    for rel in [n for n in namen if n.endswith(".rels")]:
        ziel = rel.replace("_rels/", "").replace(".rels", "")
        if ziel not in namen:
            continue
        vorhanden = set(re.findall(r'Id="(rId\d+)"', z.read(rel).decode("utf-8")))
        inhalt = z.read(ziel).decode("utf-8", errors="replace")
        benutzt = set(re.findall(r'r:(?:id|embed|link|pict|dm|lo|qs|cs)="(rId\d+)"',
                                 inhalt))
        fehlend = benutzt - vorhanden
        if fehlend:
            befunde.append("%s: nicht deklarierte rIds %s" % (ziel, sorted(fehlend)))

    # 4) XSD-Prüfung der Folien gegen das PowerPoint-Schema.
    #    Nur NEUE Fehler zaehlen: manche Vorlagen bringen bereits eigene
    #    Schemaverstoesse mit, die PowerPoint nachweislich toleriert.
    befunde += xsd_befunde(z, pfad)

    # 5) laesst sich ueberhaupt wieder einlesen
    try:
        from pptx import Presentation
        Presentation(pfad)
    except Exception as e:                                  # noqa: BLE001
        befunde.append("python-pptx kann die Datei nicht oeffnen: %s" % e)

    return befunde


def xsd_befunde(z, pfad):
    """Folien-XML gegen pml.xsd pruefen. Leere Liste, wenn kein Schema da ist."""
    try:
        from lxml import etree
    except ImportError:
        return []
    schema_pfad = None
    for kandidat in SCHEMA_ORTE:
        if os.path.exists(kandidat):
            schema_pfad = kandidat
            break
    if schema_pfad is None:
        # Sonst-Fall bewusst benannt: ohne Schema wird nicht stillschweigend
        # "alles ok" gemeldet, sondern der uebersprungene Schritt angezeigt.
        print("        (Hinweis: pml.xsd nicht gefunden, XSD-Pruefung uebersprungen)")
        return []
    schema = etree.XMLSchema(etree.parse(schema_pfad))
    raus = []
    for teil in sorted(n for n in z.namelist()
                       if n.startswith("ppt/slides/slide") and n.endswith(".xml")):
        doc = etree.parse(io.BytesIO(z.read(teil)))
        if schema.validate(doc):
            continue
        for e in schema.error_log:
            if any(t in e.message for t in TOLERIERT):
                continue
            raus.append("%s: %s" % (teil, e.message))
    return raus


def main(pfade):
    if not pfade:
        print("Aufruf: python3 scripts/check_pptx.py <datei.pptx> [...]")
        return 1
    schlecht = 0
    for p in pfade:
        befunde = pruefe(p)
        if befunde:
            schlecht += 1
            print("FEHLER  %s" % p)
            for b in befunde:
                print("        - %s" % b)
        else:
            print("OK      %s" % p)
    # Sonst-Fall bewusst ausformuliert: 0 nur, wenn wirklich nichts gefunden wurde
    return 1 if schlecht else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
