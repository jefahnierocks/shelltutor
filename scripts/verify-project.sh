#!/usr/bin/env bash
# Stable no-argument project check; the Makefile owns the native gate.
set -eu
if [ "$#" -ne 0 ]; then
    printf 'usage: scripts/verify-project.sh\n' >&2
    exit 2
fi
cd "$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd -P)"
exec make verify
