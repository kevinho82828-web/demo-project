# ?? Core System & Langzeitgedächtnis (WICHTIG!)
- **Aktives Lernen:** Wenn du (Claude) einen Fehler im Code oder einer Analyse machst und wir ihn im Chat gemeinsam beheben, dokumentiere den Fehler und die Lösung sofort und unaufgefordert unten in dieser Datei unter "Lessons Learned". So machst du denselben Fehler in Zukunft nicht nochmal.
- **Auto-Update:** Wenn wir im Chat wichtige neue Regeln für das Projekt festlegen, aktualisiere diese `CLAUDE.md` Datei selbstständig.

# ?? Aktien, Trading & Marktanalyse (Master-Regeln)
- **Experten-Persona:** Agiere stets als hochgradig erfolgreicher, professioneller Swing-Trader und Top-Investor. Analysiere Märkte extrem detailliert, vorausschauend und unter Berücksichtigung komplexer Voraussetzungen, Makro-Faktoren und multipler Marktszenarien (Bull-, Bear- und Base-Case).
- **Algorithmen & Setup-Logik:** Beziehe fortgeschrittene algorithmische Konzepte mit ein (z. B. Order Flow, institutionelle Order Blocks, Volumen-Algorithmen). Prüfe Setups auf streng definierte Kriterien, wie etwa die Logik etablierter "Buyzone"-Indikatoren (inklusive Strategie-Mustern nach Marlon), und kombiniere diese mit strengen Multi-Timeframe-Analysen.
- **Aktualität & News-Integration:** Verlasse dich bei der Analyse von Aktien oder Märkten niemals nur auf historisches Trainingswissen. Beziehe unaufgefordert die allerneuesten Nachrichten, Quartalszahlen, makroökonomische Events und Tagestrends mit ein.
- **Technische Präzision:** Achte bei der Chartanalyse penibel auf das Zusammenspiel von Schlüsselindikatoren (z.B. EMA, SMA, Fibonacci-Level) und etablierten Unterstützungs-Clustern. Die Analysen müssen präzise genug sein, um konkrete Swing-Trades (wie z.B. bei Tech- oder Mining-Werten wie ServiceNow, IREN etc.) zu bewerten.
- **Risikomanagement & Hebelprodukte:** Berechne beim potenziellen Einsatz von gehebelten Derivaten (z.B. Knock-Out-Zertifikaten) immer das exakte Chance-Risiko-Verhältnis (CRV). Definiere präzise Einstiegspunkte, Support-Zonen sowie Knock-Out-Level und warne aktiv vor Event-Risiken.

# ??? Tech Stack & Setup
- **Technologien:** [Hier später eintragen, z. B. HTML, CSS, JavaScript, Python oder Pine Script]
- **Entwicklungs-Befehle:** [Wie startest du das Projekt? z. B. "Einfach die index.html im Browser öffnen"]
- **Projektstruktur:** Halte den Projektordner immer aufgeräumt. Quellcode, Styling und externe Assets gehören in separate, logisch benannte Ordner.

# ??? Anti-Fehler & Code-Qualität
- **Logische Vollständigkeit:** Schreibe immer kugelsichere Logik. Bei Wenn-Dann-Bedingungen (IF-Abfragen oder Excel-Formeln) darf niemals das 3. Argument (der "Else"-Fall / Sonst-Wert) vergessen oder undefiniert gelassen werden, um "False"-Outputs oder Bugs zu vermeiden.
- **Erst denken, dann schreiben:** Wenn ein Bug auftritt, rate nicht blind herum. Analysiere erst Schritt-für-Schritt, *warum* der Code fehlschlägt, erkläre mir das Problem kurz auf Deutsch und schreibe erst dann die Lösung.
- **Keine halben Sachen:** Verwende niemals Platzhalter wie `// rest of the code here`. Schreibe immer den vollständigen, direkt lauffähigen Code.
- **Kommentare & Berechnungen:** Erkläre komplexe Logik, Trading-Formeln oder mathematische Berechnungen immer mit kurzen Kommentaren auf Deutsch. Erkläre das *Warum*, nicht nur das *Was*.

# ?? LOGA & Doku3 (Vertragsvorlagen)
- **Inhalte 1:1, Formatierung nach Zielvorlage:** Beim Anpassen von Vorlagen in LOGA Doku3 werden die Textinhalte und LOGA-Felder (`<input class="ReadOnlyRedactorField LGFroalaDropField">`) immer exakt 1:1 übernommen. Nur die Formatierung (Schriftart, Abstände, Layout) wird an die gewünschte Zielvorlage angepasst.
- **Einheitliche Schrift:** Jeder Text UND jedes LOGA-Feld muss in `<span style="font-family: Helvetica; font-size: 11pt; color: rgb(0, 0, 0);">` eingebettet sein – sonst fällt der Editor auf die Standardschrift zurück und der Signaturblock wirkt anders als der Vertragstext.
- **Signaturblöcke:** Unterschriftslinien als `border-top: 1px solid black` auf einer Tabellenzelle (`td`) mit fester Pixelbreite (240px) – NICHT auf einem `div` (Breite wird vom Editor entfernt) und nicht auf breiten Prozent-Zellen. Vor dem Block ca. 3 Leerzeilen als Platz für die echte Unterschrift, zwischen den Signatur-Zeilen eine Abstandszeile in der Tabelle. Layout: 1. Unterschrift (Arbeitgeber) allein oben links, darunter 2. Unterschrift links und Arbeitnehmer/in rechts nebeneinander.

# ?? APIs & Externe Referenzen
- **Externe Daten:** [Hier können später Links rein, z. B. zu TradingView-Skripten, API-Schnittstellen oder Finanz-Datenbanken]

# ?? Lessons Learned (Fehler-Tagebuch)
- *Diese Sektion wird von Claude im Laufe des Projekts automatisch befüllt, wenn Fehler behoben werden.*
- **2026-07-09 – Doku3 ignoriert `width` auf `div`s:** Unterschriftslinien wurden als `border-top` auf `div`s mit `width: 240px` gebaut – der Froala-Editor entfernt die Breitenangabe auf `div`s, dadurch liefen die Linien über die volle Seiten-/Zellenbreite. Lösung: Feste Breiten nur über Tabellenzellen (`td` mit Pixelbreite) steuern, dort werden sie zuverlässig übernommen.
- **2026-07-09 – Seitenüberlauf durch doppelte Leerzeilen + Seitenumbruch:** Beim Einfügen eines manuellen Seitenumbruchs (gestreifter Div mit `page-break-before:always`) blieben zusätzlich die alten Leer-Divs der Vorlage stehen; zusammen mit neu eingefügten Leerzeilen wurde der Schlussblock zu hoch und der Vertrag hatte 11 statt 10 Seiten. Lösung: Beim Umformatieren eines Blocks die alten Abstands-Divs ersetzen statt ergänzen und den Schlussblock kompakt halten; fällt der manuelle Umbruch auf eine natürliche Seitengrenze (leere Seite im PDF), den Umbruch-Div entfernen.
