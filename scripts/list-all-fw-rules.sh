#!/bin/bash -e
ZONES=$(flare list-zones |jq -r '.[].id')

for zone in $ZONES; do
  flare list-fw-rules --zoneid $zone |jq -r '.result[] | {rule_id: .id, rule_name: .description}'
done
