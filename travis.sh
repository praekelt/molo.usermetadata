#!/usr/bin/env bash

set -e # Exit whenever a command fails
set -x # Output commands run to see them in the Travis interface

function setup_testapp {
    molo scaffold testapp --include molo.usermetadata ^meta/
    cp test_settings.py testapp/testapp/settings/local.py
    cp -r molo/usermetadata/test_templates/ testapp/testapp/templates/
}

if [ "$TEST" == "molo_lint" ]; then
    flake8 molo
elif [ "$TEST" == "testapp_lint" ]; then
    setup_testapp
    flake8 testapp
elif [ "$TEST" == "build" ]; then
    setup_testapp
    pip install -e testapp
    py.test --cov
else
    echo "The environment variable TEST was not set correctly"
    exit 1
fi
