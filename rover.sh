#!/bin/bash

if ! command -v rover &> /dev/null; then
    echo "Error: 'rover' command not found"
    echo "To install rover, visit: https://www.apollographql.com/docs/rover/getting-started"
    echo "Or run: curl -sSL https://rover.apollo.dev/nix/latest | sh"
    exit 1
fi

echo 'Waiting for subgraphs to start up...'
sleep 3

exec rover dev --supergraph-config ./supergraph.yaml