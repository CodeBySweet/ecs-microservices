#!/bin/bash

METRIC_NAME="$1"
VALUE="$2"
SERVICE="$3"
STEP="$4"
JOB_NAME="$5"
PIPELINE_STAGE="$6"

CURRENT_TIME=$(date +%s%N)

# Set metric type based on name
if [[ "$METRIC_NAME" == *"duration"* ]]; then
  METRIC_TYPE="gauge"
  UNIT="s"
else
  METRIC_TYPE="sum"
  UNIT="1"
fi

cat <<EOF > temp-metric.json
{
  "resourceMetrics": [{
    "resource": {
      "attributes": [
        { "key": "origin", "value": { "stringValue": "github-actions" } }
      ]
    },
    "scopeMetrics": [{
      "scope": {
        "name": "ci-cd-metrics"
      },
      "metrics": [{
        "name": "$METRIC_NAME",
        "description": "GitHub Actions metric: $METRIC_NAME",
        "unit": "$UNIT",
        "$METRIC_TYPE": {
          "aggregationTemporality": "AGGREGATION_TEMPORALITY_CUMULATIVE",
          "isMonotonic": false,
          "dataPoints": [{
            "attributes": [
              { "key": "job", "value": { "stringValue": "$JOB_NAME" } },
              { "key": "service", "value": { "stringValue": "$SERVICE" } },
              { "key": "pipeline_stage", "value": { "stringValue": "$PIPELINE_STAGE" } },
              { "key": "step", "value": { "stringValue": "$STEP" } }
            ],
            "startTimeUnixNano": $CURRENT_TIME,
            "timeUnixNano": $CURRENT_TIME,
            "value": $VALUE
          }]
        }
      }]
    }]
  }]
}
EOF

curl -s -X POST http://localhost:4318/v1/metrics \
  -H "Content-Type: application/json" \
  --data-binary @temp-metric.json

rm temp-metric.json
