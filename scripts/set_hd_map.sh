#!/usr/bin/env bash
set -euo pipefail

# ---- colors ----
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # no color

# ---- argument check ----
if [[ $# -ne 1 ]]; then
  echo -e "${RED}Usage: $0 <map>${NC}"
  exit 1
fi

MAP_NAME="$1"

# ---- resolve paths relative to this script ----
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

APOLLO_PATH="$SCRIPT_DIR/../apollo-doppeltest"
FLAGFILE="$APOLLO_PATH/modules/common/data/global_flagfile.txt"
MAP_BASE="$APOLLO_PATH/modules/map/data"
MAP_PATH="$MAP_BASE/$MAP_NAME"

# ---- verify Apollo install ----
if [[ ! -f "$FLAGFILE" ]]; then
  echo -e "${RED}Error: Apollo not installed or global_flagfile.txt missing${NC}"
  exit 1
fi

# ---- verify map exists ----
if [[ ! -d "$MAP_PATH" ]]; then
  echo -e "${RED}Error: Map '$MAP_NAME' not found under modules/map/data${NC}"
  echo "Available maps:"
  find "$MAP_BASE" -mindepth 1 -maxdepth 1 -type d -printf " - %f\n"
  exit 1
fi

# ---- set HD map ----
# Drop any --map_dir previously appended so repeated runs do not pile up.
sed -i '/^--map_dir=/d' "$FLAGFILE"
printf "\n--map_dir=/apollo/modules/map/data/%s\n" "$MAP_NAME" \
  >> "$FLAGFILE"

echo -e "${GREEN}HD map set successfully:${NC}"
echo "  --map_dir=/apollo/modules/map/data/$MAP_NAME"