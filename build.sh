#!/usr/bin/env bash
set -o errexit
set -o pipefail

echo "🚀 Build - Winamax Betting Bot"

STORAGE_DIR="/opt/render/project/.render"
CHROME_DIR="${STORAGE_DIR}/chrome"
CHROMEDRIVER_DIR="${STORAGE_DIR}/chromedriver"

mkdir -p "${STORAGE_DIR}" "${CHROME_DIR}" "${CHROMEDRIVER_DIR}"

apt-get update -qq
apt-get install -y --no-install-recommends wget ca-certificates jq curl \
    libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libasound2 \
    libpango-1.0-0 libcairo2 fonts-liberation 2>/dev/null || true

# Chrome
if [ ! -f "${CHROME_DIR}/opt/google/chrome/google-chrome" ]; then
    cd "${CHROME_DIR}"
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O chrome.deb
    dpkg -x chrome.deb . 2>/dev/null || true
    rm -f chrome.deb
fi

export PATH="${CHROME_DIR}/opt/google/chrome:${PATH}"

# Chromedriver
if [ ! -f "${CHROMEDRIVER_DIR}/chromedriver" ]; then
    cd "${CHROMEDRIVER_DIR}"
    CHROME_VERSION=$("${CHROME_DIR}/opt/google/chrome/google-chrome" --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+' | head -1)
    DRIVER_URL=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" | jq -r --arg v "$CHROME_VERSION" '.channels.Stable.downloads.chromedriver[] | select(.platform=="linux64") | .url')
    wget -q "$DRIVER_URL" -O chromedriver.zip
    unzip -q chromedriver.zip
    mv chromedriver-linux64/chromedriver .
    chmod +x chromedriver
    rm -rf chromedriver.zip chromedriver-linux64
fi

export PATH="${CHROMEDRIVER_DIR}:${PATH}"

pip install --upgrade pip --quiet
pip install -r requirements.txt --no-cache-dir --prefer-binary --quiet

echo "✅ Build terminé !"
