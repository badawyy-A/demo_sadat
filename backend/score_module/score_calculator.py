# Mapping of levels to scores
LEVEL_TO_SCORE = {
    "L1": 2,
    "L2": 4,
    "L3": 6,
    "L4": 7,
    "L5": 8,
    "L6": 9,
    "L7": 10
}

# Function to determine level based on dataset
def get_level(value, dataset, age, inverse=False):
    if str(age) not in dataset:
        return "Unknown"
    
    levels = dataset[str(age)]
    sorted_levels = sorted(levels.items(), key=lambda x: x[1].get("max", float("inf")), reverse=inverse)
    
    for level, bounds in sorted_levels:
        min_val = bounds.get("min", float("-inf"))
        max_val = bounds.get("max", float("inf"))
        
        if inverse:
            if min_val <= value <= max_val:
                return level
            if value > max_val:
                return "L1"  # Worst performance
        else:
            if max_val >= value >= min_val:
                return level
            if value < min_val:
                return "L1"  # Worst performance
    
    return "L1"

# Class for processing age 5-8 tests
class Age5to8:
    def __init__(self, data, plate_data, balance_data):
        self.data = data
        self.plate_data = plate_data
        self.balance_data = balance_data
        self.results = {}

    def process_tests(self):
        age = self.data["plate_tapping"]["age"]
        level = get_level(self.data["plate_tapping"]["total_time_ms"], self.plate_data, age, inverse=True)
        self.results["plate_tapping"] = {"score": LEVEL_TO_SCORE.get(level, "Unknown"), "level": level}
        
        level = get_level(self.data["flamingo_balance"]["balance_errors"], self.balance_data, age, inverse=True)
        self.results["flamingo_balance"] = {"score": LEVEL_TO_SCORE.get(level, "Unknown"), "level": level}

# Class for processing age 9-18 tests
class Age9to18:
    def __init__(self, data, curl_up_data, push_up_data, run_data, speed_data):
        self.data = data
        self.curl_up_data = curl_up_data
        self.push_up_data = push_up_data
        self.run_data = run_data
        self.speed_data = speed_data
        self.results = {}

    def process_tests(self):
        age = self.data["curl_ups"]["age"]
        level = get_level(self.data["curl_ups"]["repetitions"], self.curl_up_data, age, inverse=False)
        self.results["curl_ups"] = {"score": LEVEL_TO_SCORE.get(level, "Unknown"), "level": level}
        
        level = get_level(self.data["push_ups"]["repetitions"], self.push_up_data, age, inverse=False)
        self.results["push_ups"] = {"score": LEVEL_TO_SCORE.get(level, "Unknown"), "level": level}
        
        level = get_level(self.data["run_600m"]["total_time_ms"], self.run_data, age, inverse=True)
        self.results["run_600m"] = {"score": LEVEL_TO_SCORE.get(level, "Unknown"), "level": level}
        
        level = get_level(self.data["dash_50m"]["total_time_ms"], self.speed_data, age, inverse=True)
        self.results["dash_50m"] = {"score": LEVEL_TO_SCORE.get(level, "Unknown"), "level": level}
