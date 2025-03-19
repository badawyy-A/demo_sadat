# backend/app.py
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import ORJSONResponse
from fastapi.responses import JSONResponse
from typing import Dict, Any, Callable
import os
import json
from cv_modules.process import process_age5_8, process_age9_18
from score_module.process import process_age_range , load_json
from recommendations_module.recommendtion import recomandations
from dotenv import load_dotenv
import time

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'recommendations_module', '.env'))
api_key = os.environ.get("GEMINI_API_KEY")

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify allowed origins here
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize app state to store user data persistently
app.state.user_data = {}

UPLOAD_FOLDER = os.path.join('uploads')
OUTPUT_FOLDER = os.path.join('outputs')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.state.upload_folder = UPLOAD_FOLDER
app.state.output_folder = OUTPUT_FOLDER

REFERENCE_DATA = {
    "plate": load_json(os.path.join('score_module', 'reference_data', 'plate.json')),
    "balance": load_json(os.path.join('score_module', 'reference_data', 'balance.json')),
    "curl_up": load_json(os.path.join('score_module', 'reference_data', 'curl_up.json')),
    "push_up": load_json(os.path.join('score_module', 'reference_data', 'pushUp.json')),
    "run": load_json(os.path.join('score_module', 'reference_data', 'run.json')),
    "speed": load_json(os.path.join('score_module', 'reference_data', 'speed.json')),
}
app.state.reference_data = REFERENCE_DATA

# Define the middleware function
async def logging_middleware(request: Request, call_next: Callable):
    start_time = time.time()

    print(f"Incoming request: {request.method} {request.url.path}")

    response = await call_next(request)

    process_time = time.time() - start_time
    formatted_process_time = "{0:.4f}".format(process_time)
    print(f"Request processing time: {formatted_process_time} seconds")
    print(f"Response status code: {response.status_code}")

    return response

# Register the middleware
app.middleware("http")(logging_middleware)


@app.post("/user_input")
async def user_input(data: Dict[str, Any], request: Request):
    """Endpoint to receive user details (age, weight, height, gender)."""
    required_keys = ('age', 'weight', 'height', 'gender')
    if not all(k in data for k in required_keys):
        raise HTTPException(status_code=400, detail="Missing user details (age, weight, height, gender)")

    try:
        user_details = {
            'age': int(data['age']),
            'weight': float(data['weight']),
            'height': float(data['height']),
            'gender': data['gender']
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid data types for user details")

    # Store user details in app.state.user_data (persistent storage)
    app.state.user_data['current_user_details'] = user_details

    return JSONResponse({"message": "User details received", "user_details": user_details}, status_code=200)


@app.post("/video_upload/{age_range}")
async def video_upload(age_range: str, request: Request, plate_video: UploadFile = File(None), balance_video: UploadFile = File(None), pushup_video: UploadFile = File(None), curlup_video: UploadFile = File(None)):
    """Endpoint to upload videos based on age range."""
    if age_range not in ['5-8', '9-18']:
        raise HTTPException(status_code=400, detail="Invalid age range. Must be '5-8' or '9-18'")

    # Retrieve user details from app.state.user_data (persistent storage)
    user_details = app.state.user_data.get('current_user_details')
    if not user_details:
        raise HTTPException(status_code=400, detail="User details are required. Please call /user_input endpoint first.")

    videos = {}
    uploaded_files = {
        '5-8': {'plate_video': plate_video, 'balance_video': balance_video},
        '9-18': {'pushup_video': pushup_video, 'curlup_video': curlup_video}
    }
    required_videos = list(uploaded_files[age_range].keys())

    for video_type in required_videos:
        video_file = uploaded_files[age_range][video_type]
        if video_file is None or video_file.filename == '':
            raise HTTPException(status_code=400, detail=f"Missing video file: {video_type}")

        video_filename = f"{user_details['age']}_{user_details['gender']}_{video_type.replace('_video','')}.mp4"
        video_path = os.path.join(app.state.upload_folder, video_filename)
        with open(video_path, "wb") as buffer:
            content = await video_file.read()
            buffer.write(content)
        videos[f"{video_type}_path"] = video_path

    app.state.user_data['current_video_paths'] = videos

    return JSONResponse({"message": "Videos uploaded successfully", "video_paths": videos}, status_code=200)


@app.get("/results")
async def get_results(request: Request):
    """Endpoint to process videos, calculate scores, and get recommendations."""

    user_details = app.state.user_data.get('current_user_details')
    video_paths = app.state.user_data.get('current_video_paths')

    if not user_details or not video_paths:
        raise HTTPException(status_code=400, detail="User details and video uploads are required. Call /user_input and /video_upload endpoints first.")

    age = user_details['age']
    output_path = app.state.output_folder
    reference_data = app.state.reference_data

    try:
        if 5 <= age <= 8:
            cv_result = process_age5_8(
                video_paths['plate_video_path'],
                video_paths['balance_video_path'],
                output_path,
                age
            )
            cv_result_path = os.path.join(output_path , 'scores_results_age5_8.json')
            process_age_range(cv_result_path, output_path, '5-8', reference_data)
            score_result_path = os.path.join(output_path , '5-8_score_result.json' )
            score_json = load_json(score_result_path)
            combined_data = {**user_details, **cv_result, **score_json}
            rec_class = recomandations(json.dumps(combined_data), api_key)
            recommendations = rec_class.get_response()
            bmi = rec_class.bmi


        elif 9 <= age <= 18:
            cv_result = process_age9_18(
                video_paths['pushup_video_path'],
                video_paths['curlup_video_path'],
                output_path,
                age
            )
            cv_result_path = os.path.join(output_path , 'scores_results_age9_18.json')
            process_age_range(cv_result_path, output_path, '9-18', reference_data)
            score_result_path = os.path.join(output_path , '9-18_score_result.json' )
            score_json = load_json(score_result_path)
            combined_data = {**user_details, **cv_result, **score_json}
            rec_class = recomandations(json.dumps(combined_data), api_key)
            recommendations = rec_class.get_response()
            bmi = rec_class.bmi
        else:
            raise HTTPException(status_code=400, detail="Invalid age for processing.")

        final_result = {
            "user_details": user_details,
            "BMI" : str(bmi),
            "test_scores": score_json,
            "recommendations": recommendations
        }
        return ORJSONResponse(content=final_result, status_code=200)

    except Exception as e:
        print(f"Error processing: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing videos and generating results: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5002, reload=True)