#!/bin/bash
# Example Usage - arguments are case sensitive and need to be exact.
# ./list-waf-rules-csv.sh contosocom CloudFlare "Cloudfalre WordPress"
ZONE_ID=$(flare list-zones |jq -r --arg s "$1" '.[] | select(.name | contains($s)) | .id')
PACKAGE_ID=$(flare list-waf-packages -z "$ZONE_ID" |jq -r --arg s "$2" '.[] | select(.name | contains($s)) | .id')
GROUP_ID=$(flare list-waf-groups -z "$ZONE_ID" -p "$PACKAGE_ID" |jq -r --arg s "$3" '.[] | select(.name | contains($s)) | .id')

flare list-waf-rules --zoneid $ZONE_ID \
                        --packageid $PACKAGE_ID \
                        --groupid $GROUP_ID \
                       | jq -r 'map({id,description})| (first | keys_unsorted) as $keys | map([to_entries[] | .value]) as $rows | $keys,$rows[] | @csv'
