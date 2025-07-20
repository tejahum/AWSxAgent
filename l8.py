


import numpy as np
import matplotlib.pyplot as plt

def simulate_drunken_star_orbit(
    M_black_hole=8e30,
    initial_pos=(1.5e11, 0),
    initial_vel=(0, 29780),
    drunk_noise=0.0001,
    dt=60,
    steps=5000
):
    """
    Simulates the orbit of a star around a black hole with quantum drunk noise.

    Parameters:
    - M_black_hole: Mass of black hole (kg)
    - initial_pos: Initial position tuple (x, y) in meters
    - initial_vel: Initial velocity tuple (vx, vy) in m/s
    - drunk_noise: Standard deviation of Gaussian noise multiplier
    - dt: Time step in seconds
    - steps: Number of simulation steps
    """
    G = 6.67430e-11
    pos = np.array(initial_pos, dtype=float)
    vel = np.array(initial_vel, dtype=float)
    positions = []

    for _ in range(steps):
        r = np.linalg.norm(pos)
        direction = pos / r
        F = -G * M_black_hole / r**2
        noise = 1 + np.random.normal(0, drunk_noise)
        acceleration = F * direction * noise
        vel += acceleration * dt
        pos += vel * dt
        positions.append(pos.copy())

    positions = np.array(positions)
    plt.figure(figsize=(8, 8))
    plt.plot(positions[:, 0], positions[:, 1], color='orange')
    plt.plot(0, 0, 'k*', markersize=15, label="Black Hole")
    plt.title("Quantum-Drunk Star Orbit Simulation")
    plt.axis("equal")
    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")
    plt.legend()
    plt.grid(True)
    plt.show()

simulate_drunken_star_orbit()


def traverse_tree(node: Dict[str, Any], visit_fn) -> None:
    """
    Recursively traverse a nested tree represented as dicts with 'children' lists.
    Calls `visit_fn(node)` for each node.
    """
    visit_fn(node)
    for child in node.get("children", []):
        traverse_tree(child, visit_fn)







import json
import boto3
import os

def lambda_handler(event, context):
    print("=" * 40)
    print("📦 Lambda LIGHT invoked")
    print("🔍 Raw event:\n", json.dumps(event, indent=2))

    try:
        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        print(f"🧾 File uploaded: s3://{bucket}/{key}")
    except Exception as e:
        print("❌ Failed to parse S3 event")
        print(str(e))
        return {"error": "bad_event_format"}

    if not key.endswith(".json"):
        print("⚠️ Skipping non-JSON file.")
        return {"status": "skipped", "reason": "non-json file"}

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
