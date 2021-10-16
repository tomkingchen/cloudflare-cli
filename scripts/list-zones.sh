#!/bin/bash
flare list-zones |jq '.[] | {zone_id: .id, zone_name: .name}'