import json

# Performance levels (Score to Level)
LEVELS = {
    (2, 3): "L1 (Work Harder)",
    (4, 5): "L2 (Must Improve)",
    (6, 6.9): "L3 (Can do Better)",
    (7, 7.9): "L4 (Good)",
    (8, 8.9): "L5 (Very Good)",
    (9, 9.9): "L6 (Athletic)",
    (10, 10): "L7 (Sports Fit)",
}

def compute_score(value, age, test_name, benchmarks, inverse=False):
    """Compute scores using age-specific min/max values, avoiding division by zero."""
    if age not in benchmarks.get(test_name, {}):
        return 2  # Return lowest score if age not found

    min_val = benchmarks[test_name][age].get("T_min", benchmarks[test_name][age].get("C_min", 0))
    max_val = benchmarks[test_name][age].get("T_max", benchmarks[test_name][age].get("C_max", 0))

    if min_val == max_val:
        return 2  # Avoid division by zero

    if inverse:  # Lower values are better (time-based tests)
        score = 2 + 8 * ((max_val - value) / (max_val - min_val)) + 0.1 * age
    else:  # Higher values are better (reps-based)
        score = 2 + 8 * ((value - min_val) / (max_val - min_val)) + 0.1 * age

    return round(min(max(score, 2), 10), 1)  # Ensure score is between 2 and 10

def get_performance_level(score):
    """Determine performance level based on the score."""
    for (low, high), level in LEVELS.items():
        if low <= score <= high:
            return level
    return "Unknown"

def process_tests(data, benchmarks):
    """Process test data with age-specific benchmarks."""
    results = {}

    for test in data:
        age = data[test]["age"]
        value = list(data[test].values())[1]  # Extract test metric
        inverse = test in ["plate_tapping", "run_600m", "dash_50m"]  # Lower time is better

        score = compute_score(value, age, test, benchmarks, inverse)
        level = get_performance_level(score)

        results[test] = {"score": score, "level": level}

    return json.dumps(results, indent=2)
