import json
import boto3
import time
import uuid
from datetime import datetime

INPUT_BUCKET = "f1p1-input-bucket"
OUTPUT_BUCKET = "f1p1-output-bucket"
LIGHT_LAMBDA_NAME = "lambda-light-function-name"  # Replace with actual name
RESULT_WAIT_TIMEOUT = 60  # seconds
POLL_INTERVAL = 5  # seconds

s3 = boto3.client("s3")
lambda_client = boto3.client("lambda")


def generate_input_payload(matrix_size=1000):
    return {
        "request_id": str(uuid.uuid4()),
        "triggered_at": datetime.utcnow().isoformat(),
        "scenario": "complex matrix workflow",
        "parameters": {
            "matrix_size": matrix_size
        }
    }


def upload_input_file(payload, key):
    s3.put_object(
        Bucket=INPUT_BUCKET,
        Key=key,
        Body=json.dumps(payload),
        ContentType="application/json"
    )
    print(f"✅ Uploaded input to s3://{INPUT_BUCKET}/{key}")


def invoke_light_lambda(bucket, key):
    print("🚀 Triggering LIGHT lambda manually (instead of S3 event)...")
    response = lambda_client.invoke(
        FunctionName=LIGHT_LAMBDA_NAME,
        InvocationType="Event",  # async
        Payload=json.dumps({
            "Records": [{
                "s3": {
                    "bucket": {"name": bucket},
                    "object": {"key": key}
                }
            }]
        })
    )
    print(f"✅ Lambda invocation status: {response['StatusCode']}")


def poll_for_result(output_key):
    print("⏳ Waiting for result...")
    start = time.time()
    while time.time() - start < RESULT_WAIT_TIMEOUT:
        try:
            response = s3.get_object(Bucket=OUTPUT_BUCKET, Key=output_key)
            result = json.loads(response['Body'].read())
            print("🎉 Result retrieved:")
            print(json.dumps(result, indent=2))
            return
        except s3.exceptions.NoSuchKey:
            print("🔄 Not ready yet, retrying...")
            time.sleep(POLL_INTERVAL)

    print("❌ Timeout: No result available after wait period.")


def main():
    matrix_size = 1000
    input_key = f"scenario_inputs/test_job_{uuid.uuid4().hex[:6]}.json"
    output_key = input_key.replace("scenario_inputs", "results")

    payload = generate_input_payload(matrix_size)

    upload_input_file(payload, input_key)

    invoke_light_lambda(INPUT_BUCKET, input_key)

    poll_for_result(output_key)


if __name__ == "__main__":
    main()
