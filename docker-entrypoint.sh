#!/bin/sh

INDEX_FILE="/app/static/index.html"

if [ -f "$INDEX_FILE" ]; then
  echo "incejtion env variable into frontend"
  
  CONFIG_STRING="window.APP_CONFIG = { VITE_APP_URL: '${VITE_APP_URL}', VITE_APP_VERSION: '${VITE_APP_VERSION}' };"
  
  sed -i "s|window.APP_CONFIG = {};|$CONFIG_STRING|g" "$INDEX_FILE"
fi

exec "$@"