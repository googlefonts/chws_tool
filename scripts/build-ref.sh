#!/bin/bash
DIFFDIR=build/diff
REFDIR=references
mkdir -p "$DIFFDIR"
add-chws -g="$DIFFDIR" -p "$@" |
  east-asian-spacing dump -o="$DIFFDIR" -r="$REFDIR" -
