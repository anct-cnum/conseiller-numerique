#!/bin/sh

set -eux

echo "PRE_BUILD"

cd front
yarn
export PATH=$(npm bin):$PATH
python build.py

echo "Ok."
