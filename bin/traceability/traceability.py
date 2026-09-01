#!/usr/bin/env python3
# GENERIERT aus personal/tools-ref/traceability/ — nicht hier editieren; Aenderungen gehoeren nach ~/.claude/tools-ref/traceability/.
# source: personal-provider-ref
# ref-hash: sha256:e76cfbc5dcf2fb98d5403fbe8552b57c92abcdd461245c305280e08ca30c8843
"""
traceability.py — prueft die Verkettung zwischen Anforderungen und Tests.

Zwei Richtungen, absichtlich verschieden hart:

    Test -> Anforderung   loest jeder Verweis auf?      BRICHT den Lauf
    Anforderung -> Test   wie viele Verweise hat sie?   Zahl ohne Schwelle

Waeren beide hart, stuende der Lauf am ersten Tag rot und wuerde binnen Wochen
umgangen. Waere keine hart, meldete ein toter Verweis nichts.

Eine dritte Haerte, unabhaengig von beiden: der Lauf berichtet immer, wieviele
Testdateien er tatsaechlich gescannt hat (siehe die Zusammenfassungszeile) -
"0 Verweise" ist fuer eine einzelne Anforderung legitim, "0 gescannte Dateien
im ganzen Repo trotz testaehnlicher Quellen" ist es nicht und bricht mit
Exit 2 ab (collect_references).

Die Regeln stehen im Skill `traceability`; hier steht ihre Umsetzung. Wo dieses
Skript laeuft und mit welchen Argumenten, steht in der CLAUDE.md des Repos.

Aufruf:
    traceability.py --spec-root docs --source contracttest
    traceability.py --selftest

Rueckgabe: 0 sauber · 1 Befunde in Richtung 1 · 2 Aufruf- oder Selbstpruefungsfehler
"""
import argparse
import hashlib
import io
import re
import sys
import tempfile
from collections import defaultdict
from contextlib import redirect_stderr
from pathlib import Path

# Muss deckungsgleich mit bin/vendor-sync.py bleiben. Bewusst dupliziert und
# nicht importiert: die Kopie liegt in einem fremden Repo und erreicht das
# Meta-Repo nicht — genau der Grund, warum sie ueberhaupt eine Kopie ist.
INJECTED = ("# GENERIERT ", "# source:", "# ref-hash:")

REQUIREMENT = re.compile(r"^### Requirement:\s*(.+?)\s*$")
TOMBSTONE = re.compile(r"^### Superseded:\s*(.+?)\s*$")
MARKER = re.compile(r"^## (ADDED|MODIFIED|REMOVED) Requirements")
IDENTIFIER = re.compile(r"^\s*`req~([a-z0-9][a-z0-9.\-]*)~(\d+)`\s*$")
SUCCESSOR = re.compile(r"^Superseded by:\s*`req~([a-z0-9][a-z0-9.\-]*)~(\d+)`\s*$")
REFERENCE = re.compile(r"\[impl->req~([a-z0-9][a-z0-9.\-]*)~(\d+)\]")

TEST_PATTERNS = ("*_test.go", "*.test.ts", "*.test.tsx", "*.spec.ts", "*.spec.tsx",
                  "*Test.java")
SOURCE_SUFFIXES = (".go", ".ts", ".tsx", ".java")

SKIP = {"node_modules", ".git", "dist", "coverage", ".pnpm-store",
        "graphify-out", "vendor", "__pycache__", "target"}

# Records (docs/records/): Personen und Meetings, verkettet ueber origin: und
# participants:. Die beiden Felder brauchen kein gemeinsames Muster - sie sind
# im Bestand eindeutig getrennt. participants: enthaelt ausschliesslich
# Personen; jeder Wert muss auf persons/{wert}.md aufloesen, ein Muster ist
# dafuer nicht noetig. origin: ist gemischt (Dateinamen, Pfade, freie Worte);
# geprueft wird dort nur, was dem Themenblock- oder Meeting-Muster entspricht:
# Kuerzel in Grossbuchstaben vor dem Datum, mit optionaler laufender Nummer
# (NWC-2026-08-11, NWC-2026-08-11-2). Das Grossbuchstaben-Praefix trennt eine
# Record-Id von den uebrigen origin:-Werten im Bestand: ein Dateiname
# (....md), ein Pfad (a/b/....md) oder ein freies Wort (rekonstruiert) faellt
# schon durchs Muster, nicht erst durch eine separate Endungspruefung.
RECORD_ID = re.compile(r"^[A-Z]{2,4}-\d{4}-\d{2}-\d{2}(-\d+)?$")
BLOCK_HEADING = re.compile(r"^### (\S+)\s*—\s*(.+?)\s*$")


def fail(text: str):
    """Aufruf- und Selbstpruefungsfehler enden mit 2, Befunde mit 1.

    Der Unterschied ist fuer das Tor wesentlich: 1 heisst "die Verkettung ist
    kaputt", 2 heisst "die Pruefung konnte gar nicht stattfinden".
    """
    print(text, file=sys.stderr)
    sys.exit(2)


class Requirement:
    def __init__(self, base, revision, title, file, line):
        self.base, self.revision, self.title = base, revision, title
        self.file, self.line = file, line


class Reference:
    def __init__(self, base, revision, file, line):
        self.base, self.revision = base, revision
        self.file, self.line = file, line


class Finding:
    def __init__(self, kind, text, file=None, line=None):
        self.kind, self.text, self.file, self.line = kind, text, file, line

    def __str__(self):
        location = f"{self.file}:{self.line}: " if self.file else ""
        return f"{location}{self.kind} — {self.text}"


# ----------------------------------------------------------------- Einlesen

def _files(root: Path, pattern):
    """rglob mit uebersprungenen Verzeichnissen — sonst dauert es in node_modules."""
    for p in root.rglob(pattern):
        if p.is_file() and not (SKIP & set(p.relative_to(root).parts[:-1])):
            yield p


def read_spec(path: Path, is_delta: bool):
    """(definitions, removed, tombstones) einer einzelnen Spec-Datei.

    In einer Delta-Spec definieren nur ADDED und MODIFIED. Was unter REMOVED
    steht, ist in der Ist-Spec definiert und verschwindet erst beim Archivieren
    — es zaehlt hier als "entfernt", nicht als Definition.
    """
    definitions, removed, tombstones = [], {}, {}
    lines = path.read_text(encoding="utf-8").split("\n")
    section = "ADDED"
    pending = None          # (title, is_tombstone, header_line)
    for line_no, line in enumerate(lines, start=1):
        m = MARKER.match(line)
        if m:
            section, pending = m.group(1), None
            continue
        m = REQUIREMENT.match(line) or TOMBSTONE.match(line)
        if m:
            pending = (m.group(1), bool(TOMBSTONE.match(line)), line_no)
            continue
        if pending is None:
            continue
        m = IDENTIFIER.match(line)
        if m:
            base, rev = m.group(1), int(m.group(2))
            title, is_tombstone, header_line = pending
            if is_tombstone:
                tombstones[base] = None
                pending = ("__tombstone__" + base, True, header_line)
            elif is_delta and section == "REMOVED":
                removed[base] = None
                pending = ("__removed__" + base, False, header_line)
            else:
                definitions.append(Requirement(base, rev, title, path, header_line))
                pending = None
            continue
        m = SUCCESSOR.match(line)
        if m and pending:
            title = pending[0]
            if title.startswith("__tombstone__"):
                tombstones[title.removeprefix("__tombstone__")] = f"req~{m.group(1)}~{m.group(2)}"
            elif title.startswith("__removed__"):
                removed[title.removeprefix("__removed__")] = f"req~{m.group(1)}~{m.group(2)}"
    return definitions, removed, tombstones


def collect_requirements(spec_root: Path):
    """Ist-Spec zuerst, Delta-Specs ueberschreiben — so gewinnt der laufende Change."""
    definitions, duplicates = {}, []
    removed, tombstones = {}, {}

    def record(defs, source_is_delta):
        for a in defs:
            previous = definitions.get(a.base)
            if previous is not None and not source_is_delta:
                duplicates.append(Finding(
                    "doppelter Kurzname",
                    f"req~{a.base} steht auch in {previous.file}:{previous.line}",
                    a.file, a.line))
                continue
            definitions[a.base] = a

    specs_dir = spec_root / "specs"
    if specs_dir.is_dir():
        for p in sorted(_files(specs_dir, "*.md")):
            d, r, t = read_spec(p, is_delta=False)
            record(d, False)
            removed.update(r)
            tombstones.update(t)

    changes = spec_root / "changes"
    if changes.is_dir():
        for p in sorted(_files(changes, "*.md")):
            if "specs" not in p.parts:
                continue
            d, r, t = read_spec(p, is_delta=True)
            record(d, True)
            removed.update(r)
            tombstones.update(t)

    return definitions, removed, tombstones, duplicates


# ------------------------------------------------------ Ungescannte Tests
#
# Ausgangspunkt: dreimal ist in dieser Arbeit dieselbe Fehlerklasse
# aufgetreten - eine Pruefung meldet Erfolg, ohne etwas geprueft zu haben. Am
# naechsten an diesem Werkzeug: TEST_PATTERNS sucht *Test.java, ein Repo hielt
# seine @Test-Methoden aber in Abstract*Testcase.java - null Treffer, null
# Verweise, gruen. "0 Verweise" ist fuer eine einzelne Anforderung legitim
# (siehe distribution); "0 gescannte Dateien im ganzen Repo, obwohl
# testaehnliche Quelldateien existieren" ist es nicht. Die Heuristik unten
# unterscheidet beides, ohne auf eine feste Namensliste angewiesen zu sein:
# sie zerlegt Datei- und Verzeichnisnamen in Woerter (camelCase/snake_case)
# und prueft, ob eines mit "test" beginnt - faengt "AbstractFooTestcase.java"
# und "tests/bar.go" gleichermassen, ohne bei "latest"/"contest"/"detest"
# anzuschlagen (die zerlegen sich nicht zu einem Wort, das mit "test" beginnt).

def _words(stem: str):
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", stem)
    return [w.lower() for w in re.split(r"[^A-Za-z0-9]+", spaced) if w]


def _looks_like_test_source(root: Path, p: Path) -> bool:
    if p.suffix not in SOURCE_SUFFIXES:
        return False
    for part in p.relative_to(root).parts[:-1]:
        if any(w.startswith("test") for w in _words(part)):
            return True
    return any(w.startswith("test") for w in _words(p.stem))


def collect_references(root: Path, extra_sources):
    """(referenzen, Zahl der gescannten Dateien) - Testdateien plus namentlich
    genannte Testhilfs-Pakete.

    Absichtlich nicht "jede Quelldatei": die Konvention verkettet Tests, und ein
    engerer Scan haelt sie wenigstens teilweise erzwingbar. Ein Vertragsszenario
    ausserhalb einer Testdatei wird ueber --source nachgereicht.

    Scannt der Lauf am Ende NICHTS (weder TEST_PATTERNS noch --source treffen),
    ist das fuer sich genommen kein Fehler - ein Repo kann legitim ganz ohne
    Tests sein. Bricht wird es erst, wenn trotzdem Dateien im Baum liegen, die
    wie Tests aussehen (_looks_like_test_source): dann hat die Pruefung nicht
    "nichts gefunden", sondern "am falschen Ort gesucht", und das ist ein
    Aufruffehler (exit 2), keine stille Null.
    """
    files = set()
    for pattern in TEST_PATTERNS:
        files.update(_files(root, pattern))
    for q in extra_sources:
        folder = (root / q).resolve()
        if not folder.is_dir():
            fail(f"FEHLER: --source zeigt auf kein Verzeichnis: {q}")
        for p in folder.rglob("*"):
            if p.is_file() and p.suffix in SOURCE_SUFFIXES:
                files.add(p)

    if not files:
        candidates = sorted(p for p in _files(root, "*")
                             if _looks_like_test_source(root, p))
        if candidates:
            listed = "\n".join(f"  - {c.relative_to(root)}" for c in candidates[:10])
            more = (f"\n  ... und {len(candidates) - 10} weitere"
                     if len(candidates) > 10 else "")
            fail(
                "FEHLER: 0 Testdateien gescannt (Muster "
                f"{', '.join(TEST_PATTERNS)}), aber Dateien, die wie Tests "
                f"aussehen, liegen unter {root}:\n{listed}{more}\n"
                "        TEST_PATTERNS passt nicht, oder --source fehlt.\n"
                "        Ein Repo ganz ohne Tests waere hier ohne solche "
                "Kandidaten durchgelaufen.")

    references = []
    for p in sorted(files):
        for line_no, line in enumerate(p.read_text(encoding="utf-8",
                                                     errors="replace").split("\n"), start=1):
            for m in REFERENCE.finditer(line):
                references.append(Reference(m.group(1), int(m.group(2)), p, line_no))
    return references, len(files)


# ----------------------------------------------------------------- Pruefen

def analyse(spec_root: Path, source_root: Path, extra_sources=()):
    definitions, removed, tombstones, findings = collect_requirements(spec_root)
    references, scanned = collect_references(source_root, extra_sources)
    findings = list(findings)
    counts = defaultdict(int)

    for r in references:
        if r.base in definitions:
            a = definitions[r.base]
            if r.revision == a.revision:
                counts[r.base] += 1
            elif r.revision < a.revision:
                findings.append(Finding(
                    "veraltete Revision",
                    f"Verweis auf req~{r.base}~{r.revision}, "
                    f"die Anforderung steht auf ~{a.revision}", r.file, r.line))
            else:
                findings.append(Finding(
                    "vorgegriffene Revision",
                    f"Verweis auf req~{r.base}~{r.revision}, "
                    f"die Anforderung steht auf ~{a.revision}", r.file, r.line))
            continue

        successor = tombstones.get(r.base, removed.get(r.base, "__missing__"))
        if successor == "__missing__":
            findings.append(Finding(
                "nicht aufloesbar",
                f"req~{r.base}~{r.revision} findet keine Anforderung",
                r.file, r.line))
        elif successor:
            findings.append(Finding(
                "abgeloest",
                f"req~{r.base} wurde abgeloest durch {successor}",
                r.file, r.line))
        else:
            findings.append(Finding(
                "abgeloest",
                f"req~{r.base} wurde entfernt, ohne Nachfolger",
                r.file, r.line))

    return definitions, counts, findings, scanned


# ----------------------------------------------------------------- Records

def _frontmatter(path: Path):
    """Liest den Frontmatter-Block: `schluessel: wert` und `schluessel: [a, b]`.

    Kein YAML-Parser - deckt nur das schmale Schema dieses Layers ab, ein Feld
    je Zeile. Gibt (felder, zeilennummern) zurueck; Letzteres, damit ein Befund
    auf die Zeile zeigen kann, die ihn ausgeloest hat.
    """
    lines = path.read_text(encoding="utf-8", errors="replace").split("\n")
    fields, field_lines = {}, {}
    if not lines or lines[0].strip() != "---":
        return fields, field_lines
    for line_no, line in enumerate(lines[1:], start=2):
        if line.strip() == "---":
            break
        m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_-]*):\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            value = [v.strip().strip("'\"") for v in inner.split(",") if v.strip()] \
                if inner else []
        else:
            value = value.strip("'\"")
        fields[key] = value
        field_lines[key] = line_no
    return fields, field_lines


def _looks_like_record_id(value: str) -> bool:
    """Themenblock- oder Meeting-Id: KUERZEL-JJJJ-MM-TT[-n], Kuerzel in Grossbuchstaben."""
    return bool(RECORD_ID.match(value))


def analyse_records(spec_root: Path, records_root: Path):
    """None, wenn records_root fehlt - dann bleibt das Werkzeug unveraendert.

    Sonst (personen, ziele, befunde): ein Ziel ist ein Meeting oder einer
    seiner Themenbloecke, je mit [titel, folgen-zaehler, ist_meeting].
    """
    if not records_root.is_dir():
        return None

    findings = []

    persons = {}
    for p in sorted(_files(records_root / "persons", "*.md")):
        fields, _ = _frontmatter(p)
        person_id = fields.get("id")
        if person_id:
            persons[person_id] = p

    targets = {}
    for p in sorted(_files(records_root / "meetings", "*.md")):
        fields, field_lines = _frontmatter(p)
        meeting_id = fields.get("id")
        if not meeting_id:
            continue
        targets[meeting_id] = [fields.get("title", ""), 0, True]

        for line in p.read_text(encoding="utf-8", errors="replace").split("\n"):
            m = BLOCK_HEADING.match(line)
            if m and _looks_like_record_id(m.group(1)):
                targets[m.group(1)] = [m.group(2), 0, False]

        participants = fields.get("participants", [])
        participant_line = field_lines.get("participants")
        for participant in participants:
            if participant not in persons:
                findings.append(Finding(
                    "participant nicht aufloesbar",
                    f"participants nennt {participant}, das keine Personen-Id findet",
                    p, participant_line))

    origin_sources = list(_files(spec_root / "changes", "proposal.md")) + \
        list(_files(spec_root / "project" / "decisions", "*.md"))

    for p in sorted(origin_sources):
        fields, field_lines = _frontmatter(p)
        origins = fields.get("origin", [])
        origin_line = field_lines.get("origin")
        is_consequence = p.name == "proposal.md" or fields.get("status") == "rejected"
        for value in origins:
            if not _looks_like_record_id(value):
                continue
            if value in targets:
                if is_consequence:
                    targets[value][1] += 1
            else:
                findings.append(Finding(
                    "origin nicht aufloesbar",
                    f"origin nennt {value}, das keine Meeting- oder Themenblock-Id findet",
                    p, origin_line))

    return persons, targets, findings


def report(definitions, counts, findings, scanned, records=None, output=sys.stdout):
    print("Verkettung\n", file=output)
    for base in sorted(definitions):
        a = definitions[base]
        print(f"  {counts[base]:>3} Verweise  req~{base}~{a.revision}  {a.title}",
              file=output)
    zero = sum(1 for b in definitions if counts[b] == 0)
    print(f"\n{len(definitions)} Anforderungen, {sum(counts.values())} Verweise aus "
          f"{scanned} Testdatei(en), {zero} ohne Verweis.", file=output)
    if records is not None:
        persons, targets = records
        print("\nRecords\n", file=output)
        for target_id in sorted(targets):
            title, count, _ = targets[target_id]
            print(f"  {count:>3} Folgen  {target_id}  {title}", file=output)
        zero_records = sum(1 for t in targets.values() if t[1] == 0)
        meetings_count = sum(1 for t in targets.values() if t[2])
        blocks_count = len(targets) - meetings_count
        print(f"\n{len(persons)} Personen, {meetings_count} Meetings, "
              f"{blocks_count} Themenbloecke, {zero_records} ohne Folgen.", file=output)
    if findings:
        print(f"\n{len(findings)} Befund(e) — der Lauf bricht:\n", file=output)
        for finding in findings:
            print(f"  {finding}", file=output)
    else:
        print("Kein toter Verweis.", file=output)


# ----------------------------------------------------------------- Selbstausweis

def _header(lines):
    start = 1 if lines and lines[0].startswith("#!") else 0
    i = start
    while i < len(lines) and (lines[i].startswith("#") or not lines[i].strip()):
        i += 1
    return start, i


def _without_injected(data: bytes) -> bytes:
    lines = data.decode("utf-8").split("\n")
    start, end = _header(lines)
    kept = [line for line in lines[start:end] if not line.startswith(INJECTED)]
    return "\n".join(lines[:start] + kept + lines[end:]).encode("utf-8")


def self_check():
    """Bricht ab, wenn diese Kopie von ihrer Referenz abweicht.

    Eine abgewichene Kopie hiesse, dass zwei Repos verschieden streng pruefen —
    und eine Zusicherung, deren Haelften sich uneinig sein koennen, sichert nichts
    zu. Laeuft das Skript aus seiner Referenz heraus, gibt es nichts auszuweisen.
    """
    this_file = Path(__file__).resolve()
    lines = this_file.read_text(encoding="utf-8").split("\n")
    start, end = _header(lines)
    recorded = None
    for line in lines[start:end]:
        content = line[1:].lstrip() if line.startswith("#") else line
        if content.startswith("ref-hash: sha256:"):
            recorded = content.split("sha256:", 1)[1].strip()
    if recorded is None:
        return                                   # Referenz, keine Kopie

    root = this_file.parent
    h = hashlib.sha256()
    for p in sorted((q for q in root.rglob("*") if q.is_file()),
                    key=lambda q: q.relative_to(root).as_posix()):
        rel = p.relative_to(root).as_posix()
        data = p.read_bytes()
        if rel == this_file.name:
            data = _without_injected(data)
        h.update(rel.encode("utf-8") + b"\0")
        h.update(hashlib.sha256(data).hexdigest().encode("ascii") + b"\0")
    if h.hexdigest() != recorded:
        fail(
            "FEHLER: diese Kopie der Verkettungspruefung weicht von ihrer Referenz ab.\n"
            "        Aenderung in tools-ref/traceability/ uebernehmen und neu zustellen.\n"
            "        Bis dahin prueft dieses Repo anders als die anderen.")


# ----------------------------------------------------------------- Selbsttest

# Sentinel statt Finding-Art: dieser Fall erwartet keinen Finding-Katalog,
# sondern dass analyse() selbst per fail() mit exit 2 abbricht.
ABORT = "__abort__"

FIXTURES = {
    "sauber": ({
        "docs/specs/zugang/spec.md":
            "### Requirement: Ohne Anmeldung kein Zugriff\n"
            "`req~zugang.ohne-anmeldung~1`\n",
        "a_test.go": "// [impl->req~zugang.ohne-anmeldung~1]\nfunc TestA(t *T){}\n",
    }, []),

    "sauber, java": ({
        "docs/specs/zugang/spec.md":
            "### Requirement: Ohne Anmeldung kein Zugriff\n"
            "`req~zugang.ohne-anmeldung~1`\n",
        "src/test/java/ZugangTest.java":
            "// [impl->req~zugang.ohne-anmeldung~1]\n"
            "class ZugangTest { void test() {} }\n",
        # Ein target/-Verzeichnis mit einer .java-Datei darf nicht mitgezaehlt
        # werden -- Maven legt so etwas bei generierten Quellen ab, und ein
        # zweiter Treffer derselben Kennung waere kein doppelter Kurzname,
        # sondern nur derselbe Bau-Output zweimal gelesen.
        "target/generated-sources/ZugangTest.java":
            "// [impl->req~zugang.ohne-anmeldung~1]\n",
    }, []),

    "nicht aufloesbar": ({
        "docs/specs/zugang/spec.md":
            "### Requirement: Ohne Anmeldung kein Zugriff\n"
            "`req~zugang.ohne-anmeldung~1`\n",
        "a_test.go": "// [impl->req~zugang.gibt-es-nicht~1]\n",
    }, ["nicht aufloesbar"]),

    "veraltete Revision": ({
        "docs/specs/zugang/spec.md":
            "### Requirement: Ohne Anmeldung kein Zugriff\n"
            "`req~zugang.ohne-anmeldung~2`\n",
        "a_test.go": "// [impl->req~zugang.ohne-anmeldung~1]\n",
    }, ["veraltete Revision"]),

    "vorgegriffene Revision": ({
        "docs/specs/zugang/spec.md":
            "### Requirement: Ohne Anmeldung kein Zugriff\n"
            "`req~zugang.ohne-anmeldung~1`\n",
        "a_test.go": "// [impl->req~zugang.ohne-anmeldung~2]\n",
    }, ["vorgegriffene Revision"]),

    "grabstein nennt nachfolger": ({
        "docs/specs/zugang/spec.md":
            "### Superseded: Ohne Anmeldung kein Zugriff\n"
            "`req~zugang.ohne-anmeldung~1`\n"
            "Superseded by: `req~zugang.rolle-entscheidet~1`\n"
            "\n### Requirement: Die Rolle entscheidet\n"
            "`req~zugang.rolle-entscheidet~1`\n",
        "a_test.go": "// [impl->req~zugang.ohne-anmeldung~1]\n",
    }, ["abgeloest"]),

    "delta-spec loest auf": ({
        "docs/changes/2026-01-01-x/specs/zugang/spec.md":
            "## ADDED Requirements\n\n### Requirement: Neu\n"
            "`req~zugang.ganz-neu~1`\n",
        "a_test.go": "// [impl->req~zugang.ganz-neu~1]\n",
    }, []),

    "doppelter kurzname": ({
        "docs/specs/zugang/spec.md":
            "### Requirement: Eins\n`req~zugang.doppelt~1`\n"
            "\n### Requirement: Zwei\n`req~zugang.doppelt~1`\n",
    }, ["doppelter Kurzname"]),

    "test ohne kennung schweigt": ({
        "docs/specs/zugang/spec.md":
            "### Requirement: Ohne Anmeldung kein Zugriff\n"
            "`req~zugang.ohne-anmeldung~1`\n",
        "a_test.go": "func TestOhneKennung(t *T){}\n",
    }, []),

    "zusatzquelle wird gelesen": ({
        "docs/specs/zugang/spec.md":
            "### Requirement: Ohne Anmeldung kein Zugriff\n"
            "`req~zugang.ohne-anmeldung~1`\n",
        "contracttest/suite.go": "// [impl->req~zugang.ohne-anmeldung~1]\n",
    }, []),

    "records: origin loest auf": ({
        "docs/records/meetings/2026-08-11-kickoff.md":
            "---\nid: NWC-2026-08-11\n---\n"
            "\n### NWC-2026-08-11-2 — Freigabeprozess\n",
        "docs/changes/2026-08-11-freigabe/proposal.md":
            "---\nstatus: draft\norigin: [NWC-2026-08-11-2]\n---\n",
    }, []),

    "records: origin ohne ziel": ({
        "docs/records/meetings/2026-08-11-kickoff.md":
            "---\nid: NWC-2026-08-11\n---\n",
        "docs/changes/2026-08-11-x/proposal.md":
            "---\nstatus: draft\norigin: [NWC-2026-08-11-9]\n---\n",
    }, ["origin nicht aufloesbar"]),

    "records: origin ohne grossbuchstaben-praefix wird ignoriert": ({
        "docs/records/meetings/.keep": "",
        "docs/changes/2026-08-11-y/proposal.md":
            "---\nstatus: draft\n"
            "origin: [2026-08-11-etwas.md, rekonstruiert]\n---\n",
    }, []),

    "records: participants loest auf": ({
        "docs/records/persons/max-mustermann.md":
            "---\nid: max-mustermann\n---\n",
        "docs/records/meetings/2026-08-11-kickoff.md":
            "---\nid: NWC-2026-08-11\nparticipants: [max-mustermann]\n---\n",
    }, []),

    "records: participants ohne person": ({
        "docs/records/meetings/2026-08-11-kickoff.md":
            "---\nid: NWC-2026-08-11\nparticipants: [erika-musterfrau]\n---\n",
    }, ["participant nicht aufloesbar"]),

    "records: meeting ohne folgen": ({
        "docs/records/meetings/2026-08-11-kickoff.md":
            "---\nid: NWC-2026-08-11\n---\n",
    }, []),

    "records: kein verzeichnis": ({
        "docs/specs/zugang/spec.md":
            "### Requirement: Ohne Anmeldung kein Zugriff\n"
            "`req~zugang.ohne-anmeldung~1`\n",
        "a_test.go": "// [impl->req~zugang.ohne-anmeldung~1]\n",
    }, []),

    # Die drei Faelle unten decken die Haertung ab: TEST_PATTERNS trifft
    # nichts, obwohl das Repo testaehnliche Quelldateien hat (ABORT, exit 2),
    # ein Repo ganz ohne Tests bleibt legitim (leer, kein Abbruch), und ein
    # haeufiges Wort, das zufaellig "test" enthaelt, loest keinen Fehlalarm
    # aus (die Wortgrenzen-Heuristik trennt "Testcase" von "Latest").

    "testaehnliche datei ohne treffer bricht ab": ({
        "docs/specs/zugang/spec.md":
            "### Requirement: Ohne Anmeldung kein Zugriff\n"
            "`req~zugang.ohne-anmeldung~1`\n",
        "src/test/java/testcases/AbstractZugangTestcase.java":
            "// [impl->req~zugang.ohne-anmeldung~1]\n"
            "abstract class AbstractZugangTestcase { }\n",
    }, [ABORT]),

    "repo ganz ohne tests bleibt legitim": ({
        "docs/specs/zugang/spec.md":
            "### Requirement: Ohne Anmeldung kein Zugriff\n"
            "`req~zugang.ohne-anmeldung~1`\n",
        "src/main/java/Zugang.java": "class Zugang {}\n",
    }, []),

    "latest ist kein testaehnlicher dateiname": ({
        "docs/specs/zugang/spec.md":
            "### Requirement: Ohne Anmeldung kein Zugriff\n"
            "`req~zugang.ohne-anmeldung~1`\n",
        "src/main/java/LatestConfig.java": "class LatestConfig {}\n",
    }, []),
}


def selftest() -> int:
    failures = []
    for name, (files, expected) in sorted(FIXTURES.items()):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel, content in files.items():
                p = root / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(content, encoding="utf-8")
            extra = ["contracttest"] if (root / "contracttest").is_dir() else []

            if expected == [ABORT]:
                # fail() schreibt nach stderr und beendet den Prozess selbst -
                # das gehoert hier abgefangen, nicht in der Ausgabe des
                # Selbsttests zu erscheinen.
                stderr = io.StringIO()
                try:
                    with redirect_stderr(stderr):
                        analyse(root / "docs", root, extra)
                    failures.append(f"  {name}: erwarteter Abbruch blieb aus")
                except SystemExit as e:
                    if e.code != 2:
                        failures.append(
                            f"  {name}: Abbruch mit Exit {e.code}, erwartet 2")
                continue

            _, counts, findings, scanned = analyse(root / "docs", root, extra)
            records = analyse_records(root / "docs", root / "docs" / "records")
            findings = findings + (records[2] if records is not None else [])
            kinds = sorted(f.kind for f in findings)
            if kinds != sorted(expected):
                failures.append(f"  {name}: erwartet {sorted(expected)}, bekommen {kinds}")
            elif name == "zusatzquelle wird gelesen" and counts["zugang.ohne-anmeldung"] != 1:
                failures.append(f"  {name}: Verweis aus der Zusatzquelle nicht gezaehlt")
            elif name == "sauber, java" and counts["zugang.ohne-anmeldung"] != 1:
                failures.append(f"  {name}: *Test.java nicht gefunden oder target/ nicht "
                                 f"uebersprungen (erwartet 1 Verweis, gezaehlt "
                                 f"{counts['zugang.ohne-anmeldung']})")
            elif name == "records: meeting ohne folgen" and (
                    records is None or records[1]["NWC-2026-08-11"][1] != 0):
                failures.append(f"  {name}: Meeting wurde nicht als Ziel mit 0 Folgen gezaehlt")
            elif name == "records: kein verzeichnis" and records is not None:
                failures.append(f"  {name}: Records-Pruefung haette uebersprungen werden muessen")
            elif name == "sauber" and scanned != 1:
                failures.append(f"  {name}: erwartet 1 gescannte Datei, gezaehlt {scanned}")
            elif name == "repo ganz ohne tests bleibt legitim" and scanned != 0:
                failures.append(f"  {name}: erwartet 0 gescannte Dateien, gezaehlt {scanned}")

    if failures:
        print(f"Selbsttest: {len(failures)} von {len(FIXTURES)} Faellen fehlgeschlagen.")
        print("\n".join(failures))
        return 2
    print(f"Selbsttest: {len(FIXTURES)} Faelle, alle gruen.")
    return 0


# ----------------------------------------------------------------- Aufruf

def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec-root", default="docs",
                    help="Verzeichnis mit specs/ und changes/ (Vorgabe: docs)")
    ap.add_argument("--source-root", default=".",
                    help="Wurzel, unter der Tests gesucht werden (Vorgabe: .)")
    ap.add_argument("--source", action="append", default=[], metavar="PATH",
                    help="zusaetzliches Verzeichnis mit Vertragsszenarien "
                         "ausserhalb von Testdateien; mehrfach erlaubt")
    ap.add_argument("--selftest", action="store_true",
                    help="nur die mitgelieferten Faelle pruefen, kein Repo lesen")
    ap.add_argument("--records-root", default="docs/records",
                    help="Verzeichnis mit Personen- und Meeting-Datensaetzen "
                         "(Vorgabe: docs/records); fehlt es, wird die "
                         "Records-Pruefung stillschweigend uebersprungen")
    args = ap.parse_args()

    self_check()

    if args.selftest:
        sys.exit(selftest())

    spec_root = Path(args.spec_root).resolve()
    if not spec_root.is_dir():
        fail(f"FEHLER: --spec-root zeigt auf kein Verzeichnis: {args.spec_root}")

    definitions, counts, findings, scanned = analyse(
        spec_root, Path(args.source_root).resolve(), args.source)

    records = analyse_records(spec_root, Path(args.records_root).resolve())
    all_findings = findings + (records[2] if records is not None else [])

    report(definitions, counts, all_findings, scanned,
           records=(records[0], records[1]) if records is not None else None)
    sys.exit(1 if all_findings else 0)


if __name__ == "__main__":
    main()
