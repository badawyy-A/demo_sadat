from fastapi import FastAPI, HTTPException,UploadFile, File
from pydantic import BaseModel, ValidationError
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

app = FastAPI()

# Allow all origins for CORS to resolve cross-origin issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (can specify frontend origin)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

class UserInput(BaseModel):
    age: int
    gender: str
    weight: float
    height: float


"""class ProcessedResults(BaseModel):
    json_path: str

class RecommendationResponse(BaseModel):
    recommended_sports: List[str]
"""


# Directory to save uploaded videos
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure the upload directory exists

@app.post("/upload-video/{test_id}")
async def upload_video(test_id: str, file: UploadFile = File(...)):
    if not file.filename.endswith((".mp4", ".avi", ".mov", ".mkv")):
        raise HTTPException(status_code=400, detail="Invalid file format. Only videos are allowed.")
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Video uploaded successfully",
        "test_id": test_id,
        "file_name": file.filename,
        "file_path": file_path
    }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)





"""
@router.post("/process_video", response_model=ProcessedResults)
async def process_uploaded_videos(video_paths: list[str]):
    json_path = process_video(video_paths)
    return {"json_path": json_path}


@router.get("/get_results")
async def get_results(json_path: str):
    with open(json_path, "r") as f:
        results = json.load(f)
    return results


@router.post("/recommend_sports", response_model=RecommendationResponse)
async def recommend_sports_endpoint(bmi: float, json_path: str, age: int, gender: str):
    recommended_sports = recommend_sports(bmi, json_path, age, gender)
    return {"recommended_sports": recommended_sports}


@router.get("/final_output")
async def final_output(json_path: str, bmi: float, age: int, gender: str):
    with open(json_path, "r") as f:
        test_results = json.load(f)
    
    recommendations = recommend_sports(bmi, json_path, age, gender)
    
    return {
        "User Info": {"Age": age, "Gender": gender, "BMI": bmi},
        "Test Results": test_results,
        "Recommended Sports": recommendations
    }"""