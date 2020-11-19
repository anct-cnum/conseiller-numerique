#!/bin/sh

set -eux

echo "PRE_BUILD"

cd front
yarn
python build.py

echo "Ok."
