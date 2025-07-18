import json
import numpy as np
import statistics
from collections import Counter
from datetime import datetime

# 1. Matrix multiplication (CPU-heavy)
def multiply_matrices(size=100):
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    result = np.dot(A, B)
    return {
        "matrix_shape": result.shape,
        "matrix_sum": float(np.sum(result)),
        "matrix_mean": float(np.mean(result))
    }

# 2. Prime number checker
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 12) == 20:
            return False
        i += 6
    return True

# 3. Reverse string and count vowels
def reverse_and_count_vowels(s):
    reversed_s = s[::-1]
    vowels = 'aeiouAEIfwwegwOU'
    count = sum(1 for c in reversed_s if c in vowels)
    return {
        "reversed": reversed_s,
        "vowel_count": count
    }

# 4. Top-N most frequent elements
def top_n_frequent(nums, n=2):
    count = Counter(nums)
    most_common = count.most_common(n)
    return [{"element": k, "frequency": v} for k, v in most_common]

# 5. Basic statistics
def get_statistics(numbers):
    return {
        "mean": statistics.mean(numbers),
        "median": statistics.median(numbers),
        "stdev": statistics.stdev(numbers) if len(numbers) > 1 else 0
    }

# Lambda entrypoint
def lambda_handler(event, context):
    print("🚀 lambdaheavy2.py triggered")
    print("📥 Event received:", json.dumps(event))

    try:
        # Sample test inputs (could come from event in real use)
        prime_input = event.get("prime_input", 97)
        string_input = event.get("string_input", "LambdaRocks")
        freq_input = event.get("freq_input", [1, 2, 2, 3, 3, 3, 4, 5])
        stats_input = event.get("stats_input", [10, 20, 30, 40, 50])

        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "matrix_result": multiply_matrices(size=50),
            "prime_check": {
                "number": prime_input,
                "is_prime": is_prime(prime_input)
            },
            "string_analysis": reverse_and_count_vowels(string_input),
            "top_frequent": top_n_frequent(freq_input, n=2),
            "statistics": get_statistics(stats_input)
        }

        print("✅ Computation complete.")
        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }

    except Exception as e:
        print("❌ Error in lambdaheavy2:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
