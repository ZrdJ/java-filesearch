#!/usr/bin/env bash
set -euo pipefail

# Devcontainer Post-Create-Hook (java-maven Template).
# Idempotent — wird bei jeder Container-Erstellung ausgefuehrt.

echo "[post-create] Fixing named-volume permissions (m2-cache)..."
# Docker-Named-Volumes werden mit root:root erstellt; der vscode-User braucht Schreibzugriff.
sudo chown -R vscode:vscode /home/vscode/.m2

# Eclipse Temurin via Adoptium apt-Repo. Hintergrund:
# Microsoft-Java-Image bringt Microsoft OpenJDK mit — manche Gradle/Plugin-Toolchains erwarten
# das Standard-JDK-Layout (JAVA_HOME/Packages, Temurin-Style). Auch generelle Distributions-
# Konsistenz mit CI (setup-java mit distribution=temurin) ist erwuenscht.
# Adoptium installiert nach /usr/lib/jvm/temurin-{ver}-jdk-amd64. devcontainer.json setzt
# JAVA_HOME entsprechend. Microsoft-OpenJDK bleibt ungenutzt parallel im Image.
TEMURIN_VERSION=25
TEMURIN_HOME="/usr/lib/jvm/temurin-${TEMURIN_VERSION}-jdk-amd64"

if [ ! -d "$TEMURIN_HOME" ]; then
    echo "[post-create] Installing Eclipse Temurin ${TEMURIN_VERSION} (Adoptium)..."
    sudo apt-get update -qq
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        wget apt-transport-https gpg >/dev/null
    wget -qO - https://packages.adoptium.net/artifactory/api/gpg/key/public \
        | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/adoptium.gpg
    echo "deb https://packages.adoptium.net/artifactory/deb bookworm main" \
        | sudo tee /etc/apt/sources.list.d/adoptium.list > /dev/null
    sudo apt-get update -qq
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        "temurin-${TEMURIN_VERSION}-jdk" >/dev/null
    echo "[post-create] Temurin ${TEMURIN_VERSION} installed at $TEMURIN_HOME."
else
    echo "[post-create] Temurin ${TEMURIN_VERSION} already present."
fi

echo "[post-create] Installing Maven via apt..."
# Microsoft-Java-Bookworm hat JDK, aber kein Maven vorinstalliert.
# `features/java:1` mit installMaven schlaegt in manchen buildx-Sandbox-Netzen am
# SDKMAN-Internet-Healthcheck fehl — apt ist robust und liefert Maven 3.8.7 (Bookworm).
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends maven >/dev/null
echo "[post-create] Maven installed: $(mvn -version 2>&1 | grep -E '^Apache Maven' | head -1)"

echo "[post-create] Java versions:"
echo "  JAVA_HOME: ${JAVA_HOME:-not set}"
echo "  active java: $(java -version 2>&1 | head -1)"

# IntelliJ Native Devcontainer Mode-Fix: das JetBrains-Backend laeuft im Container als root
# (Container-Default-User), waehrend mvn/gradle im Terminal als vscode-User laufen (devcontainer
# remoteUser). Der Indexer sucht in /root/.m2/repository/ — leer, weil Maven nach
# /home/vscode/.m2/repository/ schreibt. Folge: alle Dependencies im IntelliJ-Editor rot.
# Symlink /root/.m2 -> /home/vscode/.m2 macht beide User auf denselben m2-Cache zeigen.
# Idempotent: -f ueberschreibt eventuell vorhandenen Pfad (Dir oder Symlink).
echo "[post-create] Symlinking /root/.m2 -> /home/vscode/.m2 (IntelliJ-Backend-Fix)..."
sudo ln -sfn /home/vscode/.m2 /root/.m2

echo "[post-create] Activating pre-push hook (core.hooksPath=.githooks)..."
if git rev-parse --git-dir >/dev/null 2>&1; then
    git config core.hooksPath .githooks
    echo "[post-create] core.hooksPath=.githooks set"
else
    # Tritt typischerweise auf, wenn ein Sandbox-Worktree verwendet wird, dessen .git
    # auf einen nicht gemounteten Eltern-Pfad zeigt. Produktive Klone (normale Checkouts)
    # sind nicht betroffen.
    echo "[post-create] WARN: git dir not reachable inside container."
    echo "[post-create] WARN: Push-Block-Hook NICHT aktiv. Auf dem Host setzen:"
    echo "[post-create] WARN:   git config core.hooksPath .githooks"
fi
