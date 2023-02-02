#!/bin/bash

PYTHON_VER="python3.9"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo "Executing create_pkg.sh... "

# Create dist
cd $SCRIPT_DIR
mkdir dist_lambda/

# Create and activate virtual environment...
virtualenv -p $PYTHON_VER venv_lambda
source $SCRIPT_DIR/venv_lambda/bin/activate

# Installing python dependencies...
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
  echo "Installing dependencies..."
  echo "From: requirements.txt file exists..."
  pip install -r "$SCRIPT_DIR/requirements.txt"

else
  echo "Error: requirements.txt does not exist!"
fi

# Deactivate virtual environment...
deactivate

# Create deployment package...
echo "Creating deployment package..."
cd venv_lambda/lib/$PYTHON_VER/site-packages/
cp -r . $SCRIPT_DIR/dist_lambda
cp -r $SCRIPT_DIR/lambda_function.py $SCRIPT_DIR/dist_lambda/

# Removing virtual environment folder...
echo "Removing virtual environment folder..."
rm -rf $SCRIPT_DIR/venv_lambda

# Create deployment package
echo "Creating deployment package"
cd $SCRIPT_DIR/dist_lambda/
zip -r ../lambda_package.zip *
cd $SCRIPT_DIR

# Remove dist folder
echo "Removing virtual environment folder..."
rm -rf $SCRIPT_DIR/dist_lambda

echo "Finished script execution!"