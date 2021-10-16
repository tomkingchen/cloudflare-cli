#!/bin/bash
flare list-fw-rules --zoneid "$1" |jq -r '.result[] | {rule_id: .id, rule_name: .description}'