from fitness_tests_age_5_8 import *
from fitness_tests_age_9_18 import *
import json


def process_age5_8(plate_video_path, flamingo_video_path,output_path, age):
    plate_test = PlateTappingTest(plate_video_path)
    flamingo_test = FlamingoBalance_Score(flamingo_video_path)
    
    age_range_result = {  
        "plate_tapping": {"age": age, "total_time_ms": plate_test.run_test()},
        "flamingo_balance" : {"age": age, "balance_errors": flamingo_test.process()},
    }
    # Save to a JSON file
    json_file_path = "backend/outputs/scores_results_age5_8.json"
    with open(json_file_path, "w") as json_file:
        json.dump(score_results, json_file, indent=4)

    return age_range_result


def process_age9_18(push_ups_path , curl_ups_path, output_path, age):
    push_ups_test = PushupAnalyzer(push_ups_path)
    curl_ups_test = CurlUpsTest(curl_ups_path)
    
    age_range_result = {  
        "push_ups": {"age": age, "repetitions": push_ups_test.process()},
        "curl_ups" : {"age": age, "repetitions": curl_ups_test.process()}
        #"run_600m" : {"age": age, "total_time_ms": flamingo_test.balance_loss()},
    }
    # Save to a JSON file
    json_file_path = "backend/outputs/scores_results_age9_18.json"
    with open(json_file_path, "w") as json_file:
        json.dump(score_results, json_file, indent=4)

    return age_range_result


