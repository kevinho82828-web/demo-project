# Aufbau-Anleitung: „WeMoveHer" in SharePoint

Schritt-für-Schritt-Anleitung, um `Frauennetzwerk-Entwurf.html` mit **SharePoint-Bordmitteln** nachzubauen.
Keine Admin-Rechte, kein App-Katalog, keine Programmierung nötig — nur Bearbeitungsrechte auf der Seite.

**Zielseite:** `https://lehub.sharepoint.com/sites/DE_Intranet/HR/Vielfalt & Netzwerke/SitePages/Kopie-6.aspx`

---

## Teil 0 — Vorbereitung (vor dem ersten Klick)

Das meiste Zeitfressen beim Nachbau ist fehlendes Bildmaterial. Sammle das **vorher** und lade es in einem Rutsch in die Bildbibliothek der Seite hoch (`Websiteinhalte` → `Dokumente` → Ordner `Bilder` anlegen).

### Benötigte Bilder

| # | Bild | Verwendung | Format |
|---|---|---|---|
| 1 | Kampagnenbild „FRAUEN LENKEN ZUKUNFT!" | Hero, große Kachel | quer, min. 1200 px breit |
| 2 | Netzwerktreffen | Hero, kleine Kachel | quer |
| 3 | Mentoring | Hero, kleine Kachel | quer |
| 4 | Lunch & Learn | Hero, kleine Kachel | quer |
| 5 | Orga-Team | Hero, kleine Kachel | quer |
| 6 | Foto Netzwerktreffen (ruhig, wenig Details) | Hintergrund Zahlen-Abschnitt | quer, min. 1920 px |
| 7 | Foto Netzwerktreffen (anderes Motiv) | Hintergrund Zitat-Band | quer, min. 1920 px |
| 8 | **Fahrplan-Grafik** | Bild-Webpart | PNG, siehe unten |
| 9–12 | Netzwerktreffen · Workshop · Lunch & Learn (Screenshot) · Mentoring-Tandem | Veranstaltungsformate | quer, ca. 3:1 |
| 13 | Rote Farbfläche | Countdown-Hintergrund | PNG, einfarbig `#E2001A` |
| 14 | Rote Farbfläche oder Kampagnenbild | Call-to-Action-Hintergrund | quer |
| 15 | Teamfoto Orga-Team | Team-Abschnitt | quer, 16:9 |
| 16–18 | 1. Netzwerktreffen · Gesprächsrunde GF · Geburtstagsparty | Impressionen | quer, 4:3 |
| 19 | 11 Portraitfotos der Netzwerkerinnen | Zitate-Galerie | quadratisch |
| 20 | Rote Kachel „..und DU??" | Zitate-Galerie, letzte Kachel | quadratisch, PNG |

**Tipp zu 13 und 20:** Einfach in PowerPoint eine Folie mit rotem Hintergrund (`#E2001A`) anlegen, ggf. Text drauf, dann `Datei → Exportieren → PNG`.

### Fahrplan-Grafik erstellen

Für die Timeline gibt es **kein** natives Webpart. Sie muss ein Bild sein. Bau sie in PowerPoint nach:

- Zwei Reihen à 5 Stationen, dazwischen gestrichelte Verbindungslinie (grau `#C8C6C4`)
- Pillen-Form (abgerundetes Rechteck), Beschriftung weiß fett
- Farblogik: **erledigt** = grau `#767676` · **aktuell** = rot gefüllt `#E2001A` · **Zukunft** = weiß mit rotem Rand
- Beschriftungen exakt wie im Entwurf (Abschnitt 6)
- Als PNG exportieren, Breite mindestens 1600 px

### Kalendereinträge anlegen

Das Ereignisse-Webpart zieht seine Termine aus einer Ereignisliste. Lege sie **vorher** an:
`Websiteinhalte` → `+ Neu` → `App` → `Ereignisse`. Dann die Termine eintragen (Geburtstag 16.09., Lunch & Learn, Gesprächsrunde).

### Theme prüfen

Der Entwurf nutzt Transdev-Rot `#E2001A` als Theme-Hauptfarbe. Prüfe unter `Einstellungen (⚙️)` → `Aussehen ändern` → `Design`, ob das Corporate-Theme bereits aktiv ist.

> Falls dort nur die Microsoft-Standarddesigns stehen: Ein eigenes Farbdesign kann **nur ein Admin** per PowerShell hinzufügen. Da es sich um eine Unterseite des Konzern-Intranets handelt, ist das Transdev-Theme mit hoher Wahrscheinlichkeit schon gesetzt — dann musst du nichts tun. Die roten Überschriften kommen dann automatisch.

---

## Teil 1 — Grundprinzip

Alles läuft über denselben Dreischritt:

1. Oben rechts auf **Bearbeiten** klicken
2. Über das **⊕** am linken Rand einen **Abschnitt** hinzufügen → Spaltenlayout wählen
3. Im Abschnitt über das **⊕** ein **Webpart** einfügen

Den **Hintergrund eines Abschnitts** änderst du über das Stift-Symbol links am Abschnitt → `Abschnitt bearbeiten` → `Abschnittshintergrund`.

Die vier verfügbaren Hintergründe heißen: **Keiner · Neutral · Weiche Hervorhebung · Starke Hervorhebung**.

---

## Teil 2 — Abschnitt für Abschnitt

### ☐ 1 · Hero

- **Webpart:** Hero
- **Layout:** Kacheln, **5 Kacheln**
- Große Kachel: Bild 1, Titel `Frauennetzwerk „WeMoveHer"`, Untertitel `Das Netzwerk von Frauen für Frauen bei Transdev`
- Kleine Kacheln: Bilder 2–5 mit Titeln `Netzwerktreffen` · `Mentoring` · `Lunch & Learn` · `Orga-Team`
- Jede Kachel kann auf einen Seitenanker verlinken (siehe Hinweis zu Ankern unten)

### ☐ 2 · Quick Links

- **Abschnitt:** 1 Spalte, Hintergrund `Keiner`
- **Webpart:** Quicklinks, **Layout: Schaltfläche**

| Titel | Link |
|---|---|
| ✉️ Mitglied werden | `mailto:wemoveher@transdev.de` |
| 🗓️ Termine | Anker zum Termine-Abschnitt |
| 🥪 Lunch & Learns | Anker zum Formate-Abschnitt |
| 🚀 Mentoring | Anker zum Formate-Abschnitt |
| 📄 Ergebnisse | Dokumentbibliothek |
| 🔗 Partnernetzwerke | Unterseite |

### ☐ 3 · Intro

- **Abschnitt:** 1 Spalte, Hintergrund `Keiner`
- **Webpart:** Text, **zentriert**

> **Überschrift 2:** Ein Netzwerk von Frauen für Frauen
>
> Seit Dezember 2023 gibt es das Netzwerk WeMoveHer@transdev. Es richtet sich an **alle** weiblichen Mitarbeitenden der Transdev in Deutschland — vom Fahrdienst bis zur Führungsetage.

### ☐ 4 · Zahlen

- **Abschnitt:** 3 Spalten
- **Hintergrund:** `Bild` (Bild 6) + Überlagerung **Dunkel**
- Je Spalte ein Text-Webpart, zentriert. Zahl als **Überschrift 1**, Beschreibung als Normaltext.

| Zahl | Text |
|---|---|
| 125+ | Netzwerkerinnen aus ganz Deutschland |
| 2023 | gegründet — Teil der Unternehmensstrategie |
| 4 | Veranstaltungsformate für Austausch & Entwicklung |

> Die Schrift wird auf dunklem Hintergrund automatisch weiß.
> Falls dein SharePoint noch keine Bild-Hintergründe anbietet: Hintergrund `Starke Hervorhebung` (rot) als Ersatz nehmen.

### ☐ 5 · Ziele & Weg

- **Abschnitt:** 2 Spalten, Hintergrund `Keiner`
- Je Spalte ein Text-Webpart, **Überschrift 3** + Aufzählung

**Links — 🎯 Unsere Ziele**
```
🤝 Gegenseitige Unterstützung
📈 Berufliche Weiterentwicklung
⚖️ Förderung von Gleichberechtigung
```

**Rechts — 🛤️ Unser Weg dorthin**
```
💬 Erfahrungen untereinander austauschen und vernetzen
🌱 Sich selbst und andere weiterentwickeln
📣 Weibliche Sichtweisen innerhalb Transdev verbreite(r)n
```

> Emojis mit **Windows-Taste + Punkt** einfügen. Keine Aufzählungsformatierung verwenden — die Emojis ersetzen die Punkte.

### ☐ 6 · Wo & Wofür

- **Abschnitt:** 2 Spalten, Hintergrund **Neutral**

**Links — 📍 Wo stehen wir?**

> Wir sind schon über **125 Netzwerkerinnen**, überwiegend Fach- und Führungskräfte aus ganz Deutschland.
>
> Wir sind **Teil der Unternehmensstrategie** und leisten einen Beitrag im Themenfeld Nachhaltigkeit und Teamorientierung.
>
> Wir stehen im direkten **Austausch mit der Geschäftsführung**; unser Aufsichtsratsvorsitzender ist aktiver Unterstützer des Netzwerks.

**Rechts — 💪 Wofür stehen wir?**

> **Impulsgeberin sein:** Relevante Themen aufgreifen, Lösungsvorschläge skizzieren, als Beraterin/Sparringspartnerin zur Verfügung stehen.
>
> **Unterstützung bieten:** Geschützter Raum für Austausch, Angebote zur Förderung persönlicher und beruflicher Entwicklung.
>
> **Veränderung anstoßen:** Frauen sollen in allen Entscheidungs- und Planungsgremien vertreten sein.

### ☐ 7 · Zitat-Band

- **Abschnitt:** 1 Spalte
- **Hintergrund:** `Bild` (Bild 7) + Überlagerung **Dunkel**
- **Webpart:** Text, zentriert, **Überschrift 2 kursiv**

> *„If you have a seat at the table, open the door and let 10 more in!"*
>
> — Stimme aus dem Netzwerk

### ☐ 8 · Fahrplan

- **Abschnitt:** 1 Spalte, Hintergrund `Keiner`
- **Webpart 1:** Text

> **Überschrift 2:** Unsere Angebote / Veranstaltungsformate
>
> Um unsere Ziele zu erreichen, treffen wir uns regelmäßig virtuell oder in Präsenz und fördern den Austausch untereinander.

- **Webpart 2:** Bild → die vorbereitete Fahrplan-Grafik (Bild 8)

### ☐ 9 · Veranstaltungsformate

- **Zwei Abschnitte à 2 Spalten**, beide Hintergrund **Neutral**
- Je Spalte: **Bild-Webpart** oben (Bilder 9–12), darunter **Text-Webpart**

**Live-Netzwerktreffen**
```
• 1× pro Jahr
• Input zu festgelegtem Thema, Diskussion und Arbeitsgruppen
Ziel: intensiver Austausch, Arbeit an unseren Themen in Gruppen
```

**Arbeitsgruppen / Workshops**
```
• Einstieg, Aufstieg, Binden bei Transdev
• Netzwerk erweitern
Ziel: Lösungsansätze erarbeiten, Ergebnisse veröffentlichen, Diskussionen & Maßnahmen anstoßen
```

**Virtuelle Lunch & Learns**
```
• 1× pro Quartal
• 1-stündige Kurz-Veranstaltung in der Mittagszeit
Ziel: Input, Diskussion, Teilen von Best Practice
```

**Mentoringprogramm**
```
• Für (angehende) Führungsfrauen — 2. Runde startet im Juni 2026
• Mentoring durch Führungskräfte aus dem Topmanagement
Ziel: Wissenstransfer und gezielte Karriereförderung
```

> „Ziel:" jeweils **fett** formatieren.

### ☐ 10 · Termine & Countdown

- **Abschnitt:** 2 Spalten, Hintergrund **Weiche Hervorhebung**
- Darüber ein Text-Webpart mit **Überschrift 2**: `Nächste Termine`
- **Links:** Ereignisse-Webpart → Quelle: die in Teil 0 angelegte Ereignisliste
- **Rechts:** Countdown-Timer-Webpart
  - Titel: `Noch so lange bis zum Netzwerk-Geburtstag 🎉`
  - Zieldatum: `16.09.2026`
  - Hintergrundbild: Bild 13 (rote Fläche)

### ☐ 11 · Wie geht es weiter?

- **Abschnitt:** 3 Spalten, Hintergrund `Keiner`
- Darüber Text-Webpart, **Überschrift 2**: `Wie geht es weiter?`
- Je Spalte: Emoji groß (als **Überschrift 2**, zentriert) + **Überschrift 3** + Aufzählung

**📊 Ergebnisse**
```
Ergebnisse aus Arbeitsgruppen veröffentlichen
Diskussion der Themen, u.a. mit der Geschäftsführung
Unseren Beitrag zum Kulturwandel leisten
```

**🌱 Wachstum**
```
Netzwerk weiter ausbauen
Mitmach-Möglichkeiten für operative Mitarbeiterinnen schaffen
Sprecherinnen und Organisationsgremium weiter auf- und ausbauen
```

**🔗 Vernetzen**
```
Vernetzung ausbauen
Aktuell bereits im Austausch mit:
    WiM — Women in Mobility
    Frauennetzwerk Scheidt&Bachmann
    Gruppenweites „DEI-Network"
```

### ☐ 12 · Call to Action

- **Webpart:** Handlungsaufruf
- Hintergrundbild: Bild 14
- Ausrichtung: **Mitte**

> **Titel:** Interesse, Teil von WeMoveHer zu werden?
>
> **Text:** Alle weiblichen Mitarbeitenden der Transdev in Deutschland sind herzlich willkommen.
>
> **Schaltfläche:** `✉️ Jetzt melden: wemoveher@transdev.de` → `mailto:wemoveher@transdev.de`

### ☐ 13 · Orga-Team

- **Abschnitt:** 2 Spalten, Layout **Ein Drittel rechts**, Hintergrund **Weiche Hervorhebung**
- **Links:** Bild-Webpart (Bild 15)
- **Rechts:** Text-Webpart

> **Überschrift 3:** Das Orga-Team
>
> Von links: Annemarie Weber, Charlotte Rückert, Jessica Grossmann, Leila Steinhilper, Rebecca Reif, Sorenza Di-Piazza.
>
> Nicht im Bild: Judith Freksa, Sarah Fretter, Barbara Reinhard, Inna Thies, Ulrike von Heinemann, Marisa Bulkowski

> **Alternative:** Das **Personen-Webpart** zieht Fotos, Titel und Kontaktdaten automatisch aus dem Firmenverzeichnis — dann bleibt die Liste bei Personalwechseln aktuell.

### ☐ 14 · Impressionen

- **Abschnitt:** 3 Spalten, Hintergrund `Keiner`
- Darüber Text-Webpart, **Überschrift 2**: `Impressionen aus dem Netzwerk`
- Je Spalte ein Bild-Webpart mit Bildunterschrift (Bilder 16–18):
  `1. Netzwerktreffen in Präsenz` · `Gesprächsrunde mit der Geschäftsführung` · `1. Geburtstagsparty (16.09.)`

### ☐ 15 · Zitate-Galerie

- **Abschnitt:** 1 Spalte
- Text-Webpart, **Überschrift 2**: `Ich mache mit, weil…`
- **Webpart:** Bildergalerie, **Layout: Kacheln** — oder 3-Spalten-Abschnitte mit einzelnen Bild-Webparts

Die 11 Zitate als Bildunterschriften:
```
Netzwerk = bringt mich weiter!
MitarbeiterINNEN gewinnen & binden
Frauen bei Transdev stärken!
Barrieren finden und überwinden
einfach Ernst nehmen
Austausch, Inspiration, Female Empowerment
ohne Frauen = keine Nachhaltigkeit
Vielfalt = Zukunft · Equal Voice · Voneinander lernen
Die Stimmen der Frauen in der Transdev hörbar machen! & Gemeinsam wachsen!
If you have a seat at the table, open the door and let 10 more in!
ernst und wahrgenommen werden · Gleichberechtigung im Arbeitsalltag
```

Als 12. Kachel die rote Grafik „..und DU??" (Bild 20).

> **Empfehlung:** Einzelne Bild-Webparts in 3-Spalten-Abschnitten sehen besser aus als die Galerie, weil die Bildunterschriften dauerhaft sichtbar bleiben. In der Galerie erscheinen sie erst beim Draufzeigen.

---

## Teil 3 — Bekannte Abweichungen vom Entwurf

Ehrlich benannt, damit es beim Vergleich keine Überraschung gibt:

| Entwurf | In SharePoint | Bewertung |
|---|---|---|
| Weiße Karten mit rotem Balken oben (Formate) | Bild + Text untereinander in der Spalte, ohne Rahmen | wirkt sehr ähnlich, aber nicht identisch |
| Fahrplan als Live-Grafik | statisches PNG | inhaltlich gleich, muss bei Änderungen neu erstellt werden |
| Volle Seitenbreite bei Zitat-Band und CTA | nur auf **Kommunikationswebsites** verfügbar | auf einer Teamwebsite bleiben die Abschnitte in der Standardbreite |
| Exakte Abstände und Schriftgrößen | von SharePoint vorgegeben | nicht beeinflussbar |

Die ersten drei Punkte sind kosmetisch. Prüfe Punkt 3 zuerst: Wenn du beim Abschnittslayout die Option **Volle Breite** siehst, ist es eine Kommunikationswebsite und alles passt.

---

## Teil 4 — Seitenanker

Für die Sprungziele der Quick Links: SharePoint erzeugt Anker automatisch aus Überschriften. Der Link lautet dann

```
#unsere-ziele
```

also die Überschrift kleingeschrieben, Leerzeichen durch Bindestriche ersetzt. Bei Überschriften mit Emoji nimmt SharePoint das Emoji mit auf — deshalb steht in der Original-URL `#🎯-unsere-ziele`.

**Praktischer Weg:** Seite speichern, im Lesemodus die Zielüberschrift anfahren und den Anker aus der Adresszeile kopieren.

---

## Teil 5 — Reihenfolge

Bau nicht von oben nach unten. Effizienter:

1. **Alle Abschnitte anlegen** (Spaltenlayouts + Hintergründe) — das Gerüst
2. **Alle Texte einfügen** — inhaltlich fertig, optisch noch roh
3. **Alle Bilder einsetzen** — jetzt kommt die Wirkung
4. **Anker und Links verdrahten** — geht erst, wenn die Überschriften stehen
5. **Mobil prüfen** — Seite auf dem Handy öffnen, SharePoint stapelt Spalten automatisch

Zwischendurch immer wieder **Als Entwurf speichern**. Erst am Ende **Veröffentlichen**.
