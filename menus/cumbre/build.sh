#!/usr/bin/env bash
# Genera el PDF del menú a partir de menu.html (fuentes embebidas en assets/fonts.css)
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
CHROME="${CHROME:-/opt/pw-browsers/chromium}"
"$CHROME" --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
  --virtual-time-budget=4000 \
  --print-to-pdf="$DIR/Menu-Cumbre-RosaNegra-CDMX.pdf" \
  "file://$DIR/menu.html"
