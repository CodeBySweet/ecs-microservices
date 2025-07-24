#!/bin/bash

METRIC_NAME="$1"   # e.g., "ci_job_success" or "cd_apply_success"
VALUE="$2"         # 1 or 0 for success, or duration in seconds
SERVICE="$3"       # e.g., "all", "auth", etc.
STEP="$4"          # e.g., "build", "apply", "destroy", etc.

# Determine unit and type from metric name
if [[ "$METRIC_NAME" == *"duration"* ]]; then
  UNIT="s"
  TYPE="histogram"
else
  UNIT="1"
  TYPE="sum"
fi

# Generate metric in OpenTelemetry JSON format
cat <<EOF > temp-metric.json
{
  "resourceMetrics": [{
    "resource": {
      "attributes": [
        { "key": "service.name", "value": { "stringValue": "github-actions-runner" } }
      ]
    },
    "scopeMetrics": [{
      "metrics": [
        {
          "name": "$METRIC_NAME",
          "description": "GitHub Actions metric: $METRIC_NAME",
          "unit": "$UNIT",
          "$TYPE": {
            "dataPoints": [
              {
                "attributes": [
                  { "key": "job_name", "value": { "stringValue": "$SERVICE" } },
                  { "key": "step", "value": { "stringValue": "$STEP" } },
                  { "key": "service", "value": { "stringValue": "$SERVICE" } }
                ],
                $(if [[ "$TYPE" == "sum" ]]; then
                    echo "\"value\": $VALUE,"
                  else
                    echo "\"bucketCounts\": [0, 1],"
                    echo "\"explicitBounds\": [$VALUE],"
                  fi)
                "timeUnixNano": $(date +%s%N)
              }
            ],
            "aggregationTemporality": "AGGREGATION_TEMPORALITY_CUMULATIVE"
          }
        }
      ]
    }]
  }]
}
EOF

# Send to OpenTelemetry Collector
curl -s -X POST http://localhost:4318/v1/metrics \
  -H "Content-Type: application/json" \
  --data-binary @temp-metric.json

rm temp-metric.json
