#!/usr/bin/env bash
# Usage: ./scripts/new_project.sh <name>
set -euo pipefail
cd "$(dirname "$0")/.."
[ $# -eq 1 ] || { echo "usage: $0 <project-name>"; exit 1; }
[ -e "projects/$1" ] && { echo "projects/$1 exists"; exit 1; }
cp -r projects/_template "projects/$1"
cp prompts/edit-brief-template.md "projects/$1/brief.md"
echo "Created projects/$1. Put footage in projects/$1/raw/, fill projects/$1/brief.md, then open Claude Code in this repo."
