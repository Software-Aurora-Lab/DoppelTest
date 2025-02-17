CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT_DIRECTORY=$(dirname "$CURRENT_DIR")

# clone Apollo if not cloned
APOLLO_DIR=$PARENT_DIRECTORY/apollo-doppeltest
if [ ! -d "$APOLLO_DIR" ]; then
    git clone git@github.com:YuqiHuai/BaiduApollo.git \
        --branch DoppelTest \
        --depth 1 \
        $PARENT_DIRECTORY/apollo-doppeltest
fi

# Start Apollo
bash $PARENT_DIRECTORY/apollo-doppeltest/docker/scripts/dev_start.sh

# Build Apollo
docker exec -u $USER apollo_dev_$USER \
    bash -c \
    "source /apollo/scripts/apollo.bashrc && bash /apollo/apollo.sh build"

echo -e "\033[0;32mApollo is now built.\033[0m"