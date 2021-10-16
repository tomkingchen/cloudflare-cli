#!/bin/bash -e
ZONES=$(flare list-zones |jq -r '.[].id')
declare -A RULES ZONE_RULES

for zone in $ZONES; do
  ZONE_RULES=$(flare list-fw-rules --zoneid $zone |jq -r '[.result[] | {rule_id: .id, rule_name: .description}]')
  echo $ZONE_RULES | jq -r 'map({rule_id, rule_name}) | map([to_entries[] | .value]) as $rows | $rows[] | @csv' >> ../csv/fw_rules.csv
done
