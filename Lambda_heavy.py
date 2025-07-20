import json
import boto3
import os
import numpy as np
from datetime import datetime

s3 = boto3.client('s3')

def heavy_computation():
    print("🧮 Starting heavy computation...")
    size = 1000  # Adjust for desired heaviness (e.g., 1000x1000 matrix)
    
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    
    result = np.dot(A, B)
    
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

    response = s3.get_object(Bucket=bucket, Key=key)
    input_data = json.loads(response['Body'].read())

    print("📄 Input data loaded:", input_data)

    computation_result = heavy_computation()

    output_data = {
        "status": "processed",
        "original_key": key,
        "original_data": input_data,
        "processed_at": datetime.utcnow().isoformat(),
        "computation_result": computation_result
    }

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
