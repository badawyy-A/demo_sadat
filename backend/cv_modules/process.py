from .fitness_tests_age_5_8 import *
from .fitness_tests_age_9_18 import *
import json
import os


def process_age5_8(plate_video_path, flamingo_video_path,output_path, age):
    plate_test = PlateTappingTest(plate_video_path)
    flamingo_test = FlamingoBalance_Score(flamingo_video_path)
    plate_result = plate_test.run_test()
    print("before plate_test: ",plate_result)
    print("after: ", float(plate_result))
    age_range_result = {  
        "plate_tapping": {"age": age, "total_time_ms": plate_test.run_test()},
        "flamingo_balance" : {"age": age, "balance_errors": int(flamingo_test.process())},
    }
    # Save to a JSON file
    with open(os.path.join(output_path , 'scores_results_age5_8.json'), "w") as json_file:
        json.dump(age_range_result, json_file, indent=4)

    return age_range_result


def process_age9_18(push_ups_path , curl_ups_path, output_path, age):
    push_ups_test = PushupAnalyzer(push_ups_path)
    curl_ups_test = CurlUpsTest(curl_ups_path)
    
    age_range_result = {  
        "push_ups": {"age": age, "repetitions": int(push_ups_test.process())},
        "curl_ups" : {"age": age, "repetitions": int(curl_ups_test.process())}
        #"run_600m" : {"age": age, "total_time_ms": flamingo_test.balance_loss()},
    }
    # Save to a JSON file
    with open(os.path.join(output_path , 'scores_results_age9_18.json'), "w") as json_file:
        json.dump(age_range_result, json_file, indent=4)

    return age_range_result


