#!/bin/bash

SPAN_NAME="$1"
STATUS="$2"

# Generate trace and span IDs
TRACE_ID=$(openssl rand -hex 16)
SPAN_ID=$(openssl rand -hex 8)

# Current Unix timestamp in nanoseconds
START_TIME=$(date +%s%N)
# Simulate some work or delay here if needed
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
        "traceId": "$TRACE_ID",
        "spanId": "$SPAN_ID",
        "startTimeUnixNano": $START_TIME,
        "endTimeUnixNano": $END_TIME,
        "status": { "code": $STATUS }
      }]
    }]
  }]
}
EOF

# Send span to OpenTelemetry Collector
curl -s -X POST http://localhost:4318/v1/traces \
  -H "Content-Type: application/json" \
  --data-binary @temp-span.json

rm temp-span.json