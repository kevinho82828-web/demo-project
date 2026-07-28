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
import re
import sys
import zipfile

# Microsoft-Erweiterungs-IDs. Doppelte Werte lehnt PowerPoint ab, das
# offizielle Schema kennt diesen Namespace gar nicht.
A16_IDS = ("rowId", "colId", "creationId")


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

    # 4) laesst sich ueberhaupt wieder einlesen
    try:
        from pptx import Presentation
        Presentation(pfad)
    except Exception as e:                                  # noqa: BLE001
        befunde.append("python-pptx kann die Datei nicht oeffnen: %s" % e)

    return befunde


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
