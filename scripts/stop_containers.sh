#!/usr/bin/env bash
set -uo pipefail

# Stops and removes the containers DoppelTest creates, and nothing else.
#
# DoppelTest's runtime containers are named apollo_dev_ROUTE_<n> (one per ADS
# instance, see apollo/ApolloContainer.py) and the build container created by
# scripts/install_apollo.sh is named doppeltest_installer. Containers such as
# apollo_dev_$USER belong to other projects and are deliberately left alone.
#
# Usage: stop_containers.sh [--dry-run]

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

DRY_RUN="no"
if [[ $# -gt 0 ]]; then
  if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN="yes"
  else
    echo -e "${RED}Usage: $0 [--dry-run]${NC}"
    exit 1
  fi
fi

# Only these names are ever touched.
PATTERN='^(apollo_dev_ROUTE_[0-9]+|doppeltest_installer)$'

ALL=$(docker ps -a --format '{{.Names}}' | sort)
TARGETS=$(echo "$ALL" | grep -E "$PATTERN" || true)
OTHERS=$(echo "$ALL" | grep -vE "$PATTERN" || true)

if [[ -n "$OTHERS" ]]; then
  echo -e "${YELLOW}Leaving alone:${NC}"
  echo "$OTHERS" | sed 's/^/  - /'
fi

if [[ -z "$TARGETS" ]]; then
  echo -e "${GREEN}No DoppelTest containers to remove.${NC}"
  exit 0
fi

echo -e "${GREEN}Removing:${NC}"
echo "$TARGETS" | sed 's/^/  - /'

if [[ "$DRY_RUN" == "yes" ]]; then
  echo -e "${YELLOW}--dry-run: nothing removed.${NC}"
  exit 0
fi

# Removed one at a time: passing several names to a single `docker rm` has
# been seen to fail with "page not found" and remove nothing.
FAILED=0
while read -r name; do
  [[ -z "$name" ]] && continue
  if docker rm -f "$name" > /dev/null 2>&1; then
    echo "  removed $name"
  else
    echo -e "  ${RED}failed to remove $name${NC}"
    FAILED=1
  fi
done <<< "$TARGETS"

if [[ $FAILED -ne 0 ]]; then
  echo -e "${RED}Some containers could not be removed.${NC}"
  exit 1
fi

echo -e "${GREEN}Done.${NC}"
