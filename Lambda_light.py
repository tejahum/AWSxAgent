# === lambda_lightweight.py ===
# Triggered when new file is uploaded to input-bucket
# Validates file, then calls lambda_heavy_compute

import json
import boto3
import os

def lambda_handler(event, context):
    print("=" * 40)
    print("📦 Lambda LIGHT invoked")
    print("🔍 Raw event:\n", json.dumps(event, indent=2))

    try:
        # Step 1: Extract bucket and key
        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        print(f"🧾 File uploaded: s3://{bucket}/{key}")
    except Exception as e:
        print("❌ Failed to parse S3 event")
        print(str(e))
        return {"error": "bad_event_format"}

    # Step 2: Validate file type
    if not key.endswith(".json"):
        print("⚠️ Skipping non-JSON file.")
        return {"status": "skipped", "reason": "non-json file"}

    # Step 3: Call heavy lambda
    try:
        heavy_fn = os.environ.get("HEAVY_FUNCTION_NAME")
        if not heavy_fn:
            print("❌ HEAVY_FUNCTION_NAME not set")
            return {"error": "missing_env"}

        print(f"🚀 Invoking heavy lambda: {heavy_fn}")
        lambda_client = boto3.client("lambda")
        response = lambda_client.invoke(
            FunctionName=heavy_fn,
            InvocationType="Event",  # async
            Payload=json.dumps({"bucket": bucket, "key": key})
        )

        print("✅ Invocation complete. StatusCode:", response['StatusCode'])
        return {
            "status": "triggered",
            "bucket": bucket,
            "key": key,
            "invoke_status": response["StatusCode"]
        }

    except Exception as e:
        print("❌ Failed to invoke heavy lambda")
        print(str(e))
        return {"error": "invoke_failed"}





@tool
def analyze_pr(diff_input: str) -> str:
    """
    Parses a raw unified-diff string and reconstructs each affected Python file’s full, updated source.
    Produces and returns a JSON string with exactly two keys:
      • "summary": a one-sentence description of the PR’s purpose
      • "files": a list of objects, each with:
          – "filename": the file’s path
          – "code": the cleaned, runnable Python source for that file
    Input: diff_input (raw unified-diff text)
    Output: JSON string as specified above
    """
    # implementation…
