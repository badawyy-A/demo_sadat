from utils import process_tests

class AgeGroup9to18:
    """Handles fitness tests for ages 9-18."""
    TEST_BENCHMARKS = {
        "curl_ups": {
            9: {"C_min": 13, "C_max": 23},
            10: {"C_min": 15, "C_max": 25},
            11: {"C_min": 16, "C_max": 26},
            12: {"C_min": 16, "C_max": 27},
            13: {"C_min": 18, "C_max": 28},
            14: {"C_min": 19, "C_max": 29},
            15: {"C_min": 20, "C_max": 30},
            16: {"C_min": 20, "C_max": 30},
            17: {"C_min": 22, "C_max": 31},
            18: {"C_min": 21, "C_max": 31},
        },
        "push_ups": {
            9: {"P_min": 5, "P_max": 10},
            10: {"P_min": 6, "P_max": 11},
            11: {"P_min": 7, "P_max": 13},
            12: {"P_min": 8, "P_max": 15},
            13: {"P_min": 9, "P_max": 16},
            14: {"P_min": 10, "P_max": 17},
            15: {"P_min": 15, "P_max": 28},
            16: {"P_min": 17, "P_max": 33},
            17: {"P_min": 19, "P_max": 37},
            18: {"P_min": 21, "P_max": 43},
        },
        "run_600m": {  # Lower time is better
            9: {"T_min": 195000, "T_max": 204600},
            10: {"T_min": 192000, "T_max": 208800},
            11: {"T_min": 186000, "T_max": 202800},
            12: {"T_min": 210600, "T_max": 186000},
            13: {"T_min": 120000, "T_max": 134400},
            14: {"T_min": 150600, "T_max": 128400},
            15: {"T_min": 90600, "T_max": 94800},
            16: {"T_min": 90600, "T_max": 94200},
            17: {"T_min": 89400, "T_max": 93000},
            18: {"T_min": 85200, "T_max": 91800},
        },
        "dash_50m": {  # Lower time is better
            9: {"T_min": 8600, "T_max": 10300},
            10: {"T_min": 8300, "T_max": 10000},
            11: {"T_min": 8100, "T_max": 9700},
            12: {"T_min": 7800, "T_max": 9400},
            13: {"T_min": 7700, "T_max": 9100},
            14: {"T_min": 7600, "T_max": 8900},
            15: {"T_min": 7400, "T_max": 8700},
            16: {"T_min": 7200, "T_max": 8500},
            17: {"T_min": 7100, "T_max": 8300},
            18: {"T_min": 7000, "T_max": 8000},
        },
    }

    def __init__(self, data):
        self.data = data

    def process_tests(self):
        """Process the tests for this age group."""
        return process_tests(self.data, self.TEST_BENCHMARKS)
