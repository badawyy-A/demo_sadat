import os
from dotenv import load_dotenv
from cv_modules.process import *
from score_module.process import *
from recommendations_module.recommendtion import *

class VideoProcessor:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.reference_data = {
            "plate": load_json("score_module/reference_data/plate.json"),
            "balance": load_json("score_module/reference_data/balance.json"),
            "curl_up": load_json("score_module/reference_data/curl_up.json"),
            "push_up": load_json("score_module/reference_data/pushUp.json"),
            "run": load_json("score_module/reference_data/run.json"),
            "speed": load_json("score_module/reference_data/speed.json"),
        }
    
    def process_videos(self, user_data, output_path):
        age = user_data.get("age", 0)
        
        if age > 8:
            self._process_age9_18(user_data, output_path)
        else:
            self._process_age5_8(user_data, output_path)
    
    def _process_age9_18(self, user_data, output_path):
        process_age9_18(
            user_data['pushup_video_path'],
            user_data['curlup_video_path'],
            user_data['run_600m_video_path'],
            user_data['dash_50m_video_path'],
            output_path,
            user_data['age']
        )
        cv_result_path = os.path.join(output_path, 'scores_results_age9_18.json')
        process_age_range(cv_result_path, output_path, '9-18', self.reference_data)
        self._generate_recommendations(user_data, output_path, '9-18')
    
    def _process_age5_8(self, user_data, output_path):
        process_age5_8(
            user_data['plate_video_path'],
            user_data['balance_video_path'],
            output_path,
            user_data['age']
        )
        cv_result_path = os.path.join(output_path, 'scores_results_age5_8.json')
        process_age_range(cv_result_path, output_path, '5-8', self.reference_data)
        self._generate_recommendations(user_data, output_path, '5-8')
    
    def _generate_recommendations(self, user_data, output_path, age_group):
        score_result_path = os.path.join(output_path, f'{age_group}_score_result.json')
        score_json = load_json(score_result_path)
        rec_class = recomandations({**user_data, **score_json}, self.api_key)
        final_result = rec_class.get_response()
        print(final_result)

if __name__ == '__main__':
    processor = VideoProcessor()
    user2_data = {
        "age": 17,
        "gender": "male",
        "weight": "70",
        "height": "180",
        "pushup_video_path": "cv_modules/test_videos/plate_g.mp4",
        "curlup_video_path": "cv_modules/test_videos/plate_g.mp4",
        "run_600m_video_path": "cv_modules/test_videos/plate_g.mp4",
        "dash_50m_video_path": "cv_modules/test_videos/plate_g.mp4",
    }
    
    processor.process_videos(user2_data, 'outputs/data')
