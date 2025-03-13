from utils import process_tests

class AgeGroup5to8:
    """Handles fitness tests for ages 5-8."""
    TEST_BENCHMARKS = {
        "plate_tapping": {
            5: {"T_min": 12720, "T_max": 25250},
            6: {"T_min": 12800, "T_max": 21500},
            7: {"T_min": 12000, "T_max": 19480},
            8: {"T_min": 11370, "T_max": 17310},
        },
        "flamingo_balance": {
            5: {"E_min": 5, "E_max": 24},
            6: {"E_min": 5, "E_max": 25},
            7: {"E_min": 4, "E_max": 26},
            8: {"E_min": 5, "E_max": 26},
        },
    }

    def __init__(self, data):
        self.data = data

    def process_tests(self):
        """Process the tests for this age group."""
        return process_tests(self.data, self.TEST_BENCHMARKS)


