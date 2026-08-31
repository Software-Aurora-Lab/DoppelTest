CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIRECTORY=$(dirname "$CURRENT_DIR")

APOLLO_REPO=https://github.com/YuqiHuai/BaiduApollo.git
APOLLO_BRANCH=v7_mozart
APOLLO_DIR=$PARENT_DIRECTORY/apollo-doppeltest
# Build in a dedicated container so we never touch a system/other-project
# container (e.g. apollo_dev_$USER, which other projects use).
INSTALL_CONTAINER=doppeltest_installer

# clone Apollo if not cloned
if [ ! -d "$APOLLO_DIR" ]; then
  git clone $APOLLO_REPO \
    --branch $APOLLO_BRANCH \
    --depth 1 \
    $APOLLO_DIR
else
  # An existing checkout is left alone, but refuse to patch/build a tree that
  # is not on the expected branch.
  CURRENT_BRANCH=$(git -C $APOLLO_DIR rev-parse --abbrev-ref HEAD)
  if [ "$CURRENT_BRANCH" != "$APOLLO_BRANCH" ]; then
    echo -e "\033[0;31mError: $APOLLO_DIR is on branch '$CURRENT_BRANCH', expected '$APOLLO_BRANCH'.\033[0m"
    echo "Switch it over, or remove the directory and re-run this script:"
    echo "  git -C $APOLLO_DIR remote set-branches --add origin $APOLLO_BRANCH"
    echo "  git -C $APOLLO_DIR fetch --depth 1 origin $APOLLO_BRANCH"
    echo "  git -C $APOLLO_DIR checkout $APOLLO_BRANCH"
    exit 1
  fi
fi

# Directories DoppelTest reads/writes from the host. They are created here
# (instead of inside the container) so DoppelTest can remove Apollo's logs.
mkdir -p $APOLLO_DIR/data/log $APOLLO_DIR/data/bag $APOLLO_DIR/data/core $APOLLO_DIR/records

# Install the DoppelTest-specific files the v7_mozart branch does not carry:
#   scripts/bootstrap_doppeltest.sh - starts/stops the modules under test
#   modules/custom_nodes            - simplified_planning node
# This must happen before the build so bazel picks up the changes.
cp -a $PARENT_DIRECTORY/apollo_patches/. $APOLLO_DIR/
chmod +x $APOLLO_DIR/scripts/bootstrap_doppeltest.sh

# Start Apollo
# --fastest skips the map/other docker volumes, which would otherwise shadow
# the HD maps installed by scripts/install_hd_maps.sh
DEV_CONTAINER=$INSTALL_CONTAINER \
  bash $APOLLO_DIR/docker/scripts/dev_start.sh -l -y --fastest || exit 1

# Build Apollo
docker exec -u $USER $INSTALL_CONTAINER \
  bash -c \
  "source /apollo/scripts/apollo.bashrc && bash /apollo/apollo.sh build"
BUILD_STATUS=$?

# The build output lives in $APOLLO_DIR/.cache on the host, so the installer
# container is disposable. DoppelTest starts its own apollo_dev_ROUTE_*
# containers at runtime.
if [ $BUILD_STATUS -eq 0 ]; then
  docker rm -f $INSTALL_CONTAINER > /dev/null
  echo -e "\033[0;32mApollo is now built.\033[0m"
else
  echo -e "\033[0;31mBuild failed. Container $INSTALL_CONTAINER left running for debugging.\033[0m"
  echo "Remove it with: docker rm -f $INSTALL_CONTAINER"
  exit $BUILD_STATUS
fi
