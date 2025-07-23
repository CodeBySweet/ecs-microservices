#!/bin/bash

METRIC_NAME="$1"
METRIC_VALUE="$2"
SERVICE="$3"
JOB_NAME="$4"

cat <<EOF | curl -sS --data-binary @- http://localhost:4318/v1/metrics -H "Content-Type: application/json"
{
  "resourceMetrics": [{
    "resource": {
      "attributes": [
        { "key": "service.name", "value": { "stringValue": "$SERVICE" } },
        { "key": "job.name", "value": { "stringValue": "$JOB_NAME" } }
      ]
    },
    "scopeMetrics": [{
      "metrics": [{
        "name": "$METRIC_NAME",
        "type": "gauge",
        "gauge": {
          "dataPoints": [{
            "asDouble": $METRIC_VALUE,
            "attributes": [
              { "key": "job", "value": { "stringValue": "$JOB_NAME" } },
              { "key": "service", "value": { "stringValue": "$SERVICE" } }
            ]
          }]
        }
      }]
    }]
  }]
}
EOF
