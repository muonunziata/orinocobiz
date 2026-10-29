#!/bin/bash
# Genera el paquete importable del portal. Uso: ./make.sh [salida.zip]
set -e
cd "$(dirname "$0")"
OUT=$(realpath -m "${1:-../orinoco-wakoo.zip}")
python3 build.py pack
rm -f "$OUT"
(cd pack && zip -qrX9 "$OUT.tmp" wakoo-pack.json images fonts styles -x '*.DS_Store') && mv "$OUT.tmp" "$OUT"
ls -la "$OUT"
