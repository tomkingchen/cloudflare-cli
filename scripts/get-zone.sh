#!/bin/bash
# Find site/zone name contains certain string and output zone id and name.
flare list-zones |jq --arg s "$1" '.[] | select(.name | contains($s)) | {zoneid: .id, name: .name}'