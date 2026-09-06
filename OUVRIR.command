#!/bin/zsh
# Lance le serveur local (port 8770) si besoin et ouvre le design system dans le navigateur par défaut (Arc).
cd "$(dirname "$0")"
if ! lsof -iTCP:8770 -sTCP:LISTEN >/dev/null 2>&1; then
  nohup python3 serve.py 8770 >/dev/null 2>&1 &
  sleep 1
fi
open "http://localhost:8770/DESIGN_SYSTEM.html"
