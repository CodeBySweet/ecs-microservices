#!/bin/bash

JOB_NAME="$1"   # e.g., "ci"
SUCCESS="$2"    # 1 for success, 0 for failure
DURATION="$3"   # in seconds
STEP="$4"       # e.g., "build", "scan", "deploy"

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
          "name": "ci_job_success",
          "description": "GitHub Actions job success status",
          "unit": "1",
          "sum": {
            "dataPoints": [
              {
                "attributes": [
                  { "key": "job_name", "value": { "stringValue": "$JOB_NAME" } },
                  { "key": "step", "value": { "stringValue": "$STEP" } }
                ],
                "value": $SUCCESS,
                "timeUnixNano": $(date +%s%N)
              }
            ],
            "aggregationTemporality": "AGGREGATION_TEMPORALITY_CUMULATIVE"
          }
        },
        {
          "name": "ci_job_duration_seconds",
          "description": "GitHub Actions job duration in seconds",
          "unit": "s",
          "histogram": {
            "dataPoints": [
              {
                "attributes": [
                  { "key": "job_name", "value": { "stringValue": "$JOB_NAME" } },
                  { "key": "step", "value": { "stringValue": "$STEP" } }
                ],
                "bucketCounts": [0, 1],
                "explicitBounds": [$DURATION],
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

# Send metric to OpenTelemetry Collector
curl -s -X POST http://localhost:4318/v1/metrics \
  -H "Content-Type: application/json" \
  --data-binary @temp-metric.json

rm temp-metric.json
