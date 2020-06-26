#!/bin/sh

echo "1. Generating configuration using confd"
cp -R /app/config/saml /etc/confd
/confd -onetime -backend env

# Wait until metadata is built
echo "2. Sleeping until metadata is built"
sleep 5

export FLASK_APP=flask_sp/__init__.py
export FLASK_ENV=production
export FLASK_DEBUG=0

echo "2. Initializing IdP metadata using $LOCAL_METADATA_PATH and InCommon Metadata Service"
python -m flask recreate-tables
python -m flask init-metadata $LOCAL_METADATA_PATH

echo "3. Running the app"
python -m flask run --host 0.0.0.0 --port 80