#!/bin/bash
set -ue

find docs/notes/assets/ -maxdepth 1 -type d ! -name "*.assets" ! -name "." ! -name "assets" -exec rm -rf {} \;
