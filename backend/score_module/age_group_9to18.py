from utils import process_tests

class AgeGroup9to18:
    """Handles fitness tests for ages 9-18."""
    TEST_BENCHMARKS = {
        "curl_ups": {
            9: {"C_min": 9, "C_max": 15},
            10: {"C_min": 10, "C_max": 20},
            11: {"C_min": 12, "C_max": 22},
            12: {"C_min": 14, "C_max": 24},
            13: {"C_min": 15, "C_max": 26},
            14: {"C_min": 17, "C_max": 28},
            15: {"C_min": 18, "C_max": 30},
            16: {"C_min": 19, "C_max": 32},
            17: {"C_min": 20, "C_max": 34},
            18: {"C_min": 21, "C_max": 35},
        },
        "push_ups": {
            9: {"P_min": 4, "P_max": 10},
            10: {"P_min": 5, "P_max": 11},
            11: {"P_min": 6, "P_max": 13},
            12: {"P_min": 7, "P_max": 15},
            13: {"P_min": 8, "P_max": 16},
            14: {"P_min": 9, "P_max": 17},
            15: {"P_min": 13, "P_max": 23},
            16: {"P_min": 15, "P_max": 28},
            17: {"P_min": 17, "P_max": 33},
            18: {"P_min": 19, "P_max": 43},
        },
        "run_600m": {  # Lower time is better
            9: {"T_min": 75000, "T_max": 270000},
            10: {"T_min": 72000, "T_max": 260000},
            11: {"T_min": 70000, "T_max": 250000},
            12: {"T_min": 68000, "T_max": 240000},
            13: {"T_min": 66000, "T_max": 230000},
            14: {"T_min": 64000, "T_max": 220000},
            15: {"T_min": 62000, "T_max": 210000},
            16: {"T_min": 60000, "T_max": 200000},
            17: {"T_min": 58000, "T_max": 190000},
            18: {"T_min": 56000, "T_max": 180000},
        },
        "dash_50m": {  # Lower time is better
            9: {"T_min": 6800, "T_max": 11000},
            10: {"T_min": 6600, "T_max": 10800},
            11: {"T_min": 6400, "T_max": 10600},
            12: {"T_min": 6200, "T_max": 10400},
            13: {"T_min": 6000, "T_max": 10200},
            14: {"T_min": 5800, "T_max": 10000},
            15: {"T_min": 5600, "T_max": 9800},
            16: {"T_min": 5400, "T_max": 9600},
            17: {"T_min": 5200, "T_max": 9400},
            18: {"T_min": 5000, "T_max": 9200},
        },
    }

    def __init__(self, data):
        self.data = data

    def process_tests(self):
        """Process the tests for this age group."""
        return process_tests(self.data, self.TEST_BENCHMARKS)
