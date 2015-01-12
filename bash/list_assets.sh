#!/bin/sh

curl \
    -H "Bork-Token: $BORK_TOKEN" \
    -H "Bork-Username: $BORK_USERNAME" \
    http://api.zonza.tv:8080/v0/item
