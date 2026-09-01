# Release erstellen

## Schritt-fuer-Schritt

### 1. Version in pom.xml erhoehen

```xml
<version>0.5.0</version>
```

### 2. Aenderungen committen und pushen

```bash
git add pom.xml
git commit -m "Prepare release 0.5.0"
git push origin main
```

### 3. GitHub Release erstellen

Via CLI:

```bash
gh release create 0.5.0 \
  --repo Owner/Repo \
  --title "0.5.0" \
  --notes "## Changes
- Feature A
- Fix B
- Update dependencies"
```

Via GitHub UI:
1. Repository → Releases → "Create a new release"
2. Tag: `0.5.0` (neuen Tag erstellen)
3. Title: `0.5.0`
4. Release Notes schreiben
5. "Publish release"

### 4. Automatisierung abwarten

Nach dem Release passiert automatisch:

1. **JitPack Build** - `trigger-jitpack` Job startet den Build
2. **README Update** - `update-readme` Job aktualisiert die Version

### 5. Verifizieren

```bash
# Workflow-Status pruefen
gh run list --repo Owner/Repo --workflow=release.yml --limit=1

# JitPack Build-Status
curl -s "https://jitpack.io/api/builds/com.github.Owner/Repo/0.5.0" | jq
```

## Versionierung

- **SemVer** - `MAJOR.MINOR.PATCH`
- **Kein v-Praefix** - `0.5.0`, nicht `v0.5.0`
- **pom.xml und Tag muessen uebereinstimmen**

## Haeufige Fehler

| Problem | Loesung |
|---------|---------|
| JitPack Build failed | Build-Log pruefen: `https://jitpack.io/#Owner/Repo/0.5.0` |
| Version nicht gefunden | Tag und pom.xml Version muessen identisch sein |
| README nicht aktualisiert | `contents: write` Permission pruefen |
