#!/bin/bash
flare list-zones | jq -r 'map({id,name})| (first | keys_unsorted) as $keys | map([to_entries[] | .value]) as $rows | $keys,$rows[] | @csv'