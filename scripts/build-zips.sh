#!/bin/sh
# Rebuild dist/<skill>.zip for every skill (for uploading to the Claude app). Run from the repo root.
set -e
cd "$(dirname "$0")/.."
rm -rf dist && mkdir -p dist
for dir in plugins/*/skills/*/; do
  name=$(basename "$dir")
  (cd "$(dirname "$dir")" && zip -qr -X "../../../dist/$name.zip" "$name" -x '*/__pycache__/*' '*.pyc' '*.DS_Store')
  echo "dist/$name.zip"
done
