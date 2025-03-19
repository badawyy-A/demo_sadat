from .fitness_tests_age_5_8 import *
from .fitness_tests_age_9_18 import *
import json
import os



def process_age5_8(plate_video_path, flamingo_video_path ,output_path, age):
    plate_test = PlateTappingTest(plate_video_path)
    flamingo_test = FlamingoBalance_Score(flamingo_video_path)
    plate_result = plate_test.run_test()

    age_range_result = {  
        "plate_tapping": {"age": age, "total_time_ms": plate_test.run_test()},
        "flamingo_balance" : {"age": age, "balance_errors": int(flamingo_test.process())},
    }
    # Save to a JSON file
    with open(os.path.join(output_path , 'scores_results_age5_8.json'), "w") as json_file:
        json.dump(age_range_result, json_file, indent=4)

    return age_range_result



def process_age9_18(push_ups_path , curl_ups_path, run_walk_video_path , speed_video_path, output_path, age):
    push_ups_test = PushupAnalyzer(push_ups_path)
    curl_ups_test = CurlUpsTest(curl_ups_path)

    run_walk_600 = Running_Score(run_walk_video_path)
    total_time_ms1 , total_distance1 = run_walk_600.process_video()

    speed_50_dash = Running_Score(speed_video_path)
    total_time_ms2 , total_distance2 = speed_50_dash.process_video()

    walk_600_result = (total_time_ms1 * 600) / total_distance1
    dash_50_result = (total_time_ms2 * 50) / total_distance2
    
    age_range_result = {  
        "push_ups": {"age": age, "repetitions": int(push_ups_test.process())},
        "curl_ups" : {"age": age, "repetitions": int(curl_ups_test.process())},
        "run_600m" : {"age": age, "total_time_ms": walk_600_result},
        "dash_50m" : {"age": age, "total_time_ms": dash_50_result},
    }
    # Save to a JSON file
    with open(os.path.join(output_path , 'scores_results_age9_18.json'), "w") as json_file:
        json.dump(age_range_result, json_file, indent=4)

    return age_range_result

