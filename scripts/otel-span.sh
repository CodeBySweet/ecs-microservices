#!/bin/bash

NAME="$1"
STATUS="$2"  # OK or ERROR

curl -X POST http://localhost:4317/v1/traces \
  -H 'Content-Type: application/json' \
  -d '{
    "resourceSpans": [{
      "resource": { "attributes": [{ "key": "service.name", "value": { "stringValue": "github-actions" } }] },
      "instrumentationLibrarySpans": [{
        "spans": [{
          "name": "'"$NAME"'",
          "startTimeUnixNano": '$(($(date +%s%N)))',
          "endTimeUnixNano": '$(($(date +%s%N)))',
          "status": { "code": "'"$STATUS"'" }
        }]
      }]
    }]
  }'
