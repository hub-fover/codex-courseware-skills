#!/usr/bin/env bash
set -euo pipefail

source_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills"
target_dir="${HOME}/.codex/skills"
mkdir -p "$target_dir"

for skill_dir in "$source_dir"/*; do
  [ -d "$skill_dir" ] || continue
  name="$(basename "$skill_dir")"
  destination="$target_dir/$name"
  if [ -e "$destination" ]; then
    read -r -p "Replace existing $name? [y/N] " answer
    [[ "$answer" =~ ^[Yy]([Ee][Ss])?$ ]] || continue
    rm -rf "$destination"
  fi
  cp -R "$skill_dir" "$destination"
  printf 'Installed %s\n' "$name"
done
