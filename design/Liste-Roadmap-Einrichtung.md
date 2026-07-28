# Variante 4 einrichten: Liste „Netzwerk-Roadmap" mit Kartenformatierung

Anleitung für den Abschnitt „Wie geht es weiter?" als SharePoint-Liste mit JSON-Kartenformatierung.

**Benötigte Rechte:** Besitzerin der Website oder der Liste. **Kein** Admin, **kein** App-Katalog.
**Zeitaufwand:** ca. 20–30 Minuten einmalig.

---

## Schritt 1 — Liste anlegen

`Websiteinhalte` → `+ Neu` → `Liste` → `Leere Liste`

- **Name:** `Netzwerk-Roadmap`
- **In Websitenavigation anzeigen:** Haken **entfernen** (die Liste soll nicht im Menü auftauchen)

---

## Schritt 2 — Spalten anlegen

> ⚠️ **Wichtigster Punkt der ganzen Anleitung:** Lege die Spalten **exakt** mit diesen Namen an — ohne Leerzeichen, ohne Umlaute. SharePoint merkt sich intern den Namen, den die Spalte bei der *Erstellung* hatte. Eine Spalte „Punkt 1" mit Leerzeichen heißt intern `Punkt_x0020_1`, und dann findet die JSON-Vorlage sie nicht. Umbenennen im Nachhinein hilft nicht.

| Spaltenname | Typ | Hinweis |
|---|---|---|
| `Title` | — | schon vorhanden, enthält den Bereichsnamen |
| `Symbol` | Eine Textzeile | ein Emoji |
| `Status` | Auswahl | siehe unten |
| `Punkt1` | Eine Textzeile | |
| `Punkt2` | Eine Textzeile | darf leer bleiben |
| `Punkt3` | Eine Textzeile | darf leer bleiben |
| `Reihenfolge` | Zahl | steuert die Sortierung |

**Auswahlmöglichkeiten für `Status`** — ebenfalls exakt so schreiben, die Vorlage vergleicht auf Kleinschreibung:

```
läuft
geplant
fortlaufend
```

Bei `Status` zusätzlich die Option **„Auswahl kann manuell hinzugefügt werden"** deaktivieren, damit keine Tippfehler entstehen.

> Die Spalte `Title` heißt in der Anzeige noch „Titel". Du kannst sie über `Spalteneinstellungen → Bearbeiten` in „Bereich" umbenennen — der interne Name bleibt `Title`, die Vorlage funktioniert weiter.

---

## Schritt 3 — Inhalte eintragen

Drei Einträge:

| Title | Symbol | Status | Punkt1 | Punkt2 | Punkt3 | Reihenfolge |
|---|---|---|---|---|---|---|
| Ergebnisse | 📊 | läuft | Ergebnisse aus Arbeitsgruppen veröffentlichen | Diskussion der Themen, u.a. mit der Geschäftsführung | Unseren Beitrag zum Kulturwandel leisten | 1 |
| Wachstum | 🌱 | geplant | Netzwerk weiter ausbauen | Mitmach-Möglichkeiten für operative Mitarbeiterinnen schaffen | Sprecherinnen und Organisationsgremium weiter auf- und ausbauen | 2 |
| Vernetzen | 🔗 | fortlaufend | Vernetzung über Transdev hinaus ausbauen | Bestehende Partnerschaften vertiefen | Gemeinsame Formate mit anderen Netzwerken entwickeln | 3 |

Emojis fügst du mit **Windows-Taste + Punkt** ein.

---

## Schritt 4 — Ansicht auf Galerie umstellen

Oben rechts in der Liste auf den Ansichtsnamen klicken (steht meist auf „Alle Elemente") → **Aktuelle Ansicht formatieren**.

Im rechten Bereich:

1. **Layout** auf **Galerie** umstellen
2. Auf **Karte formatieren** klicken
3. Ganz unten auf **Erweiterter Modus** wechseln
4. Das vorhandene JSON **komplett markieren und löschen**
5. Den Inhalt von `Roadmap-Karten.view.json` einfügen
6. **Speichern**

Die Karten sollten sofort erscheinen.

---

## Schritt 5 — Sortierung festlegen

Noch in der Ansicht: auf die Spalte `Reihenfolge` klicken → **Kleinste zuerst**.
Dann Ansichtsname anklicken → **Ansicht speichern unter** → Name z.B. `Karten`.

---

## Schritt 6 — Auf die Seite bringen

Zurück auf `Kopie-6.aspx` → **Bearbeiten** → an der gewünschten Stelle einen **1-Spalten-Abschnitt** anlegen.

1. Text-Webpart einfügen, **Überschrift 2**: `Wie geht es weiter?`
2. Darunter **Liste**-Webpart einfügen
3. Liste `Netzwerk-Roadmap` auswählen
4. Im Webpart-Bearbeitungsbereich (Stift) die Ansicht **`Karten`** wählen
5. **Befehlsleiste ausblenden** aktivieren — sonst steht „+ Neu" über den Karten
6. Abschnittshintergrund auf **Weiche Hervorhebung** setzen

---

## Anpassungen

**Farben ändern** — im JSON kommen diese Werte vor:

| Wert | Bedeutung |
|---|---|
| `#E2001A` | Transdev-Rot: linker Balken und Aufzählungspunkte |
| `#FCEBED` / `#B80015` | Chip „läuft" — Hintergrund / Schrift |
| `#EFF6FC` / `#005A9E` | Chip „geplant" |
| `#F3F2F1` / `#605E5C` | Chip „fortlaufend" |

**Kartengröße ändern** — ganz oben im JSON:
```json
"height": 250,
"width": 340,
```

**Vierten Punkt ergänzen** — Spalte `Punkt4` anlegen, dann im JSON den kompletten Block von `Punkt3` kopieren und beide Vorkommen von `Punkt3` in `Punkt4` ändern.

**Weitere Statuswerte** — die Vorlage prüft zuerst auf `läuft`, dann auf `geplant`, alles andere bekommt automatisch das graue Design. Ein neuer Wert funktioniert also sofort, nur eben in Grau.

---

## Wenn etwas nicht klappt

| Symptom | Ursache |
|---|---|
| Karten sind leer | Spaltennamen stimmen nicht — prüfe die internen Namen (siehe unten) |
| Chip immer grau | Statuswert weicht ab, z.B. Großschreibung oder Leerzeichen am Ende |
| Nur eine Karte pro Zeile | Kartenbreite zu groß für den Abschnitt — `width` verkleinern |
| „+ Neu" steht über den Karten | Befehlsleiste im Webpart ausblenden (Schritt 6.5) |
| Fehlermeldung beim Speichern | JSON unvollständig eingefügt — geschweifte Klammern am Anfang und Ende prüfen |

**Internen Spaltennamen herausfinden:** Liste öffnen → `Einstellungen` → `Listeneinstellungen` → auf die Spalte klicken. In der Adresszeile steht am Ende `&Field=Punkt1`. Das ist der interne Name.

---

## Was ich nicht prüfen konnte

Ich habe keinen Zugriff auf eure SharePoint-Umgebung, konnte die Vorlage also **nicht gegen ein echtes SharePoint testen**. Das JSON ist syntaktisch validiert und folgt dem offiziellen Schema, aber zwei Punkte solltest du beim ersten Einfügen im Blick behalten:

- **`text-transform`** beim Status-Chip: Falls SharePoint diese CSS-Eigenschaft in eurer Version nicht durchlässt, erscheint der Text in normaler Schreibweise statt in Großbuchstaben. Rein kosmetisch — der Rest funktioniert.
- **`font-family`**: Wird möglicherweise ignoriert, dann greift die SharePoint-Standardschrift. Das ist ohnehin Segoe UI, fällt also nicht auf.

Wenn beim Einfügen etwas anders aussieht als erwartet, beschreib mir was du siehst — dann passe ich die Vorlage an.
