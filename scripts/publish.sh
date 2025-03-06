#!/bin/bash

# Exit on error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Cleaning up existing builds...${NC}"
rm -rf build/ dist/ *.egg-info/

echo -e "${YELLOW}Running tests...${NC}"
python -m pytest

echo -e "${YELLOW}Running type checks...${NC}"
python -m mypy shadeform/

echo -e "${YELLOW}Running style checks...${NC}"
python -m flake8 shadeform/
python -m black --check shadeform/
python -m isort --check-only shadeform/

echo -e "${YELLOW}Building package...${NC}"
python -m build

echo -e "${YELLOW}Checking package...${NC}"
python -m twine check dist/*

if [ "$1" == "--test" ]; then
    echo -e "${YELLOW}Uploading to TestPyPI...${NC}"
    python -m twine upload --repository testpypi dist/*
    
    echo -e "${GREEN}Package published to TestPyPI!${NC}"
    echo -e "Install with: pip install --index-url https://test.pypi.org/simple/ shadeform"
elif [ "$1" == "--prod" ]; then
    echo -e "${RED}Uploading to PyPI...${NC}"
    read -p "Are you sure you want to publish to PyPI? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python -m twine upload dist/*
        echo -e "${GREEN}Package published to PyPI!${NC}"
        echo -e "Install with: pip install shadeform"
    else
        echo -e "${RED}Aborted${NC}"
        exit 1
    fi
else
    echo -e "${RED}Please specify --test or --prod${NC}"
    exit 1
fi