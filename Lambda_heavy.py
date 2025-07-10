import json
import boto3
import os
import numpy as np
from datetime import datetime

s3 = boto3.client('s3')

def heavy_computation():
    print("🧮 Starting heavy computation...")
    size = 1000  # Adjust for desired heaviness (e.g., 1000x1000 matrix)
    
    # Random matrices
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    
    # Matrix multiplication (this is CPU-heavy)
    result = np.dot(A, B)
    
    # For brevity, we'll only return a summary
    computation_summary = {
        "shape": result.shape,
        "sum": float(np.sum(result)),
        "mean": float(np.mean(result))
    }
    
    print("✅ Heavy computation done.")
    return computation_summary

def lambda_handler(event, context):
    print("🧠 Heavy Lambda Started")
    print("📥 Event received:", json.dumps(event))

    bucket = event["bucket"]
    key = event["key"]

    # Step 1: Download input from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    input_data = json.loads(response['Body'].read())

    print("📄 Input data loaded:", input_data)

    # Step 2: Do some heavy computation
    computation_result = heavy_computation()

    # Step 3: Create output
    output_data = {
        "status": "processed",
        "original_key": key,
        "original_data": input_data,
        "processed_at": datetime.utcnow().isoformat(),
        "computation_result": computation_result
    }

    # Step 4: Upload result to output bucket
    output_key = key.replace("scenario_inputs", "results")
    output_bucket = "f1p1-output-bucket"

    s3.put_object(
        Bucket=output_bucket,
        Key=output_key,
        Body=json.dumps(output_data),
        ContentType="application/json"
    )

    print(f"✅ Output written to s3://{output_bucket}/{output_key}")
    return {"status": "success"}
