from fitness_tests_age_5_8 import *
from fitness_tests_age_9_18 import *

def process_age5_8(plate_video_path, flamingo_video_path,output_path, age):
    plate_test = PlateTappingTest(plate_video_path)
    flamingo_test = FlamingoBalance(flamingo_video_path)
 
    age_range_result = {  
        "plate test": plate_test.run_test(),
        "flamingo test" : flamingo_test.balance_loss(),
        "age": age
    }

    return age_range_result


def process_age9_18(output_path, age):
    pass

#"plate_tapping": {"age": 6, "total_time_ms": 14000},  
    #"flamingo_balance": {"age": 6, "balance_errors": 8}  