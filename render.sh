#!/usr/bin/env zsh

parallel -j 6 '
  class=$(sed -n "s/^class \([A-Za-z]*\)(.*/\1/p" {})
  echo "Rendering $class from {} ..."
  venv/bin/manim-slides render {} "$class"
' ::: scenes/s*.py

echo "Done. All scenes rendered."