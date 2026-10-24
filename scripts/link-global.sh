#!/usr/bin/env bash
# Link every skill in this repository into the global OpenCode skills directory.
# Existing links are replaced; real directories are never touched.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_dir="$repo_root/skills"
target_dir="${OPENCODE_SKILLS_DIR:-$HOME/.config/opencode/skills}"

mkdir -p "$target_dir"

for skill_dir in "$source_dir"/*/; do
  [ -f "$skill_dir/SKILL.md" ] || continue
  name="$(basename "$skill_dir")"
  target="$target_dir/$name"

  if [ -L "$target" ]; then
    rm "$target"
  elif [ -e "$target" ]; then
    echo "skip $name: $target exists and is not a symlink" >&2
    continue
  fi

  ln -s "$skill_dir" "$target"
  echo "linked $name -> $target"
done
