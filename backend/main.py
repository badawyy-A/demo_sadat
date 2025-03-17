from cv_modules.process import *
from score_module.process import *
from recommendations_module.recommendtion import *
import os 



user1_data = {
    "age":6,
    "gender":"male",
    "weight":"40",
    "height":"140",
    "plate_video_path":"cv_modules/test_videos/flag_g.mp4",
    "balance_video_path":"cv_modules/test_videos/flag_g.mp4"
}

user2_data = {
    "age":17,
    "gender":"male",
    "weight":"70",
    "height":"180",
    "pushup_video_path":"",
    "curlup_video_path":""
}

# Load all reference data once (Improves efficiency)
REFERENCE_DATA = {
    "plate": load_json("score_module/reference_data/plate.json"),
    "balance": load_json("score_module/reference_data/balance.json"),
    "curl_up": load_json("score_module/reference_data/curl_up.json"),
    "push_up": load_json("score_module/reference_data/pushUp.json"),
    "run": load_json("score_module/reference_data/run.json"),
    "speed": load_json("score_module/reference_data/speed.json"),
}


def video_processing(user_data , output_path , REFERENCE_DATA ):
    if user_data['age'] > 8 :
        process_age9_18(user_data['pushup_video_path'] , user_data['curlup_video_path'] ,output_path, user_data['age'])
        cv_result_path = os.path.join(output_path , 'scores_results_age9_18.json')
        process_age_range(cv_result_path ,output_path , '9-18' , REFERENCE_DATA )
        score_result_path = os.path.join(output_path , '9_18_score_result.json' )
        score_json = load_json(score_result_path)
        rec_class = recomandations({user_data**score_json}) 
        final_result = rec_class.get_response()
        print(final_result)
    else:
        process_age5_8(user_data['plate_video_path'] , user_data['balance_video_path'] ,output_path, user_data['age'])
        cv_result_path = os.path.join(output_path , 'scores_results_age5_8.json')
        process_age_range(cv_result_path ,output_path , '5-8' , REFERENCE_DATA )
        score_result_path = os.path.join(output_path , '5_8_score_result.json' )
        score_json = load_json(score_result_path)
        rec_class = recomandations({user_data**score_json}) 
        final_result = rec_class.get_response()
        print(final_result)

        

if __name__ == '__main__':
    video_processing(user1_data , 'outputs/data')