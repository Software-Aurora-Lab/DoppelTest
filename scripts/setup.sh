ENV_NAME="doppeltest"
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT_DIRECTORY=$(dirname "$CURRENT_DIR")

# exit if conda is not installed
if ! command -v conda &> /dev/null
then
    echo "Conda is not installed. Exiting..."
    exit 1
fi

BASE_DIR=$(conda info --base)
PIP="$BASE_DIR/envs/$ENV_NAME/bin/pip"

# create conda env decictor if not exist
if ! conda info --envs | grep -q "$ENV_NAME"
then
    echo "Creating conda enviroment $ENV_NAME"
    conda create -n $ENV_NAME python=3.8.10 -y
else
    echo "Conda envviroment $ENV_NAME exists"
fi

# install decictor dependencies
echo "Installing dependencies"
$PIP install -r $PARENT_DIRECTORY/requirements.txt

echo -e "\033[0;32mConda environment $ENV_NAME is now ready.\033[0m"
