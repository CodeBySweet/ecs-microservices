#!/bin/bash

SPAN_NAME="$1"
STATUS="$2"

# Current Unix timestamp in nanoseconds
START_TIME=$(date +%s%N)
END_TIME=$(date +%s%N)

cat <<EOF > temp-span.json
{
  "resourceSpans": [{
    "resource": {
      "attributes": [
        { "key": "service.name", "value": { "stringValue": "github-actions-runner" } },
        { "key": "host.name", "value": { "stringValue": "$(hostname)" } }
      ]
    },
    "scopeSpans": [{
      "spans": [{
        "name": "$SPAN_NAME",
        "startTimeUnixNano": $START_TIME,
        "endTimeUnixNano": $END_TIME,
        "status": { "code": "$STATUS" }
      }]
    }]
  }]
}
EOF

# Send span to OpenTelemetry Collector on localhost
curl -s -X POST http://localhost:4317/v1/traces \
  -H "Content-Type: application/json" \
  --data-binary @temp-span.json

rm temp-span.json
