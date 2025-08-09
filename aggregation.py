import json
import boto3
import pandas as pd

def lambda_handler(event, context):
    s3 = boto3.client("s3")
    input_bucket = event["bucket"]
    input_key = event["input_key"]
    expected_total = event.get("expected_total", 1000)

    try:
        obj = s3.get_object(Bucket=input_bucket, Key=input_key)
        df = pd.read_csv(obj["Body"])

        if "forecast" not in df.columns:
            return {
                "status": "error",
                "message": "Missing 'forecast' column in input file"
            }

        actual_total = df["forecast"].sum()
        error_margin = abs(actual_total - expected_total)

        return {
            "status": "ok" if error_margin < 50 else "warn",
            "actual_total": actual_total,
            "expected_total": expected_total,
            "error_margin": error_margin
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }