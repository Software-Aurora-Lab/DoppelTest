#!/usr/bin/env bash
set -euo pipefail

# ---- colors ----
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # no color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

APOLLO_PATH="$SCRIPT_DIR/../apollo-doppeltest"
MAP_SRC="$SCRIPT_DIR/../data/maps"
MAP_DST="$APOLLO_PATH/modules/map/data"

# Check Apollo install
if [[ ! -d "$APOLLO_PATH" ]]; then
  echo -e "${RED}Error: Baidu Apollo 7.0 not installed${NC}"
  exit 1
fi

# Check map data
if [[ ! -d "$MAP_SRC" ]]; then
  echo -e "${RED}Error: Apollo map data not found at ../data/maps${NC}"
  exit 1
fi

mkdir -p "$MAP_DST"

# Copy each map individually. The destination directory itself is left in
# place: it holds Apollo's BUILD file, which bazel targets such as
# //modules/map/data:borregas_ave depend on.
for map_path in "$MAP_SRC"/*/; do
  map_name="$(basename "$map_path")"
  rm -rf "${MAP_DST:?}/$map_name"
  cp -a "$map_path" "$MAP_DST/$map_name"
done

echo -e "${GREEN}Map data successfully copied.${NC}"
echo
echo "Installed Apollo maps:"
echo "----------------------"

find "$MAP_DST" -mindepth 1 -maxdepth 1 -type d -printf " - %f\n"
