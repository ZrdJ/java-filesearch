# Release Workflow

## GitHub Actions: release.yml

```yaml
name: Release

on:
  release:
    types: [published]

jobs:
  trigger-jitpack:
    name: Trigger JitPack Build
    runs-on: ubuntu-latest
    steps:
      - name: Trigger JitPack build
        run: |
          # Erster Request triggert den Build
          curl -s "https://jitpack.io/com/github/${{ github.repository_owner }}/${{ github.event.repository.name }}/${{ github.event.release.tag_name }}/build.log" || true
          # Kurz warten und Status pruefen
          sleep 10
          curl -s "https://jitpack.io/api/builds/com.github.${{ github.repository_owner }}/${{ github.event.repository.name }}/${{ github.event.release.tag_name }}" || true

  update-readme:
    name: Update README Version
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: main

      - name: Update version in README
        run: |
          sed -i 's/<version>.*<\/version>/<version>${{ github.event.release.tag_name }}<\/version>/g' README.md

      - name: Commit and push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add README.md
          git diff --staged --quiet || git commit -m "Update README to version ${{ github.event.release.tag_name }}"
          git push
```

## Jobs erklaert

### trigger-jitpack

- **Zweck**: JitPack Build sofort starten, nicht erst beim ersten Dependency-Abruf
- **Funktionsweise**: HTTP Request an JitPack triggert den Build
- **Vorteil**: Nutzer muessen nicht auf den Build warten

### update-readme

- **Zweck**: README zeigt immer die aktuelle Version
- **Funktionsweise**: sed ersetzt alle `<version>...</version>` Tags
- **Hinweis**: Nur commiten wenn sich etwas geaendert hat (`git diff --staged --quiet ||`)

## Voraussetzungen

- Workflow braucht `contents: write` Permission (Default fuer `GITHUB_TOKEN`)
- Release Tag muss ohne `v`-Praefix sein (z.B. `0.5.0`, nicht `v0.5.0`)
