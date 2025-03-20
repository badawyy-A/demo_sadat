# Fitness Assessment and Sport Recommendation System

## 📌 Project Overview

This project is a comprehensive **Fitness Assessment and Sport Recommendation System** designed to evaluate candidates' fitness levels (ages 5-18) and suggest suitable sports based on their performance.  It leverages **computer vision** for automated video analysis of fitness tests and an **AI-powered recommendation engine** (using Google's Gemini API) to provide personalized sport suggestions. The system is built with a modular backend (Python) and an interactive frontend (Streamlit and React.js).

## 🚀 Features

*   **Automated Fitness Assessment:**  Analyzes video recordings of standardized fitness tests using YOLOv8 pose estimation.
*   **Age-Specific Tests:** Supports different tests for two age groups:
    *   **Ages 5-8:** Plate Tapping (coordination) and Flamingo Balance Test.
    *   **Ages 9-18:** Push-ups, Curl-ups, 600m Run/Walk, and 50m Dash.
*   **AI-Powered Recommendations:**  Uses Google's Gemini API to generate personalized sport recommendations based on the assessed fitness attributes and a knowledge base of sport requirements.
*   **User-Friendly Interface:**  A Streamlit and React.js web application provides an intuitive interface for:
    *   Entering candidate details (age, gender, weight, height).
    *   Uploading video recordings of fitness tests.
    *   Viewing calculated scores and performance levels.
    *   Receiving top 3 sport recommendations.
*   **BMI Calculation:** Automatically calculates and displays the candidate's Body Mass Index (BMI).
*   **Modular Design:**  Well-structured code with separate modules for computer vision, scoring, recommendations, and the Streamlit UI, making it easy to maintain and extend.
*   **JSON Output:**  Saves intermediate results (CV analysis and scores) to JSON files for further analysis or integration with other systems.

## 📊 Usage (Workflow)

1.  **Candidate Information:** The user (e.g., a coach) enters the candidate's age, gender, weight, and height.
2.  **Video Upload:** Based on the candidate's age, the user is prompted to upload the appropriate video recordings of the required fitness tests.
3.  **Automated Analysis:** The system processes the uploaded videos using YOLOv8 pose estimation to extract relevant performance metrics (e.g., repetitions, time, balance errors).
4.  **Scoring:** The extracted metrics are compared against age- and gender-specific benchmarks (currently using *placeholder* data – **see Important Notes below**) to determine performance levels and scores.
5.  **Recommendation Generation:**  The calculated scores, along with the candidate's information, are sent to the Gemini API, which provides a ranked list of the top 3 recommended sports.
6.  **Results Display:** The Streamlit app displays the calculated BMI, individual test scores, performance levels, and the top 3 recommended sports.

## 🧠 Technologies Used

*   **Backend:**
    *   Python 3.9
    *   OpenCV (`opencv-python`)
    *   NumPy (`numpy`)
    *   Pandas (`pandas`)
    *   SciPy (`scipy`)
    *   Scikit-learn (`scikit-learn`)
    *   Ultralytics YOLOv8 (`ultralytics`)
    *   LangChain (with Google Gemini API integration: `langchain-google-genai`)
    *   python-dotenv (`python-dotenv`)
*   **Frontend:**
    *   Streamlit (`streamlit`)
* **Dependencies Management:** requirements.txt

## 📂 Project Structure
```fitness_app/
├── .env # Environment variables (Gemini API Key)
├── main.py # Main backend logic (VideoProcessor class)
├── cv_modules/ # Computer Vision Modules
│ ├── init.py
│ ├── process.py # Video processing dispatcher
│ ├── fitness_tests_age_5_8.py # CV logic for 5-8 age group
│ ├── fitness_tests_age_9_18.py # CV logic for 9-18 age group
│ ├── pose_model.py # YOLOv8 pose estimation
│ └── yolo11x-pose.pt # YOLOv8 pose estimation model file
├── score_module/ # Scoring Logic
│ ├── init.py
│ ├── process.py # Scoring logic
│ ├── score_calculator.py # Age specific score calculators (PLACEHOLDER)
│ └── reference_data/ # Reference data for scoring (PLACEHOLDER)
│ ├── plate.json # (PLACEHOLDER - Add your actual data)
│ ├── balance.json # (PLACEHOLDER - Add your actual data)
│ ├── curl_up.json # (PLACEHOLDER - Add your actual data)
│ ├── pushUp.json # (PLACEHOLDER - Add your actual data)
│ ├── run.json # (PLACEHOLDER - Add your actual data)
│ └── speed.json # (PLACEHOLDER - Add your actual data)
├── recommendations_module/ # Recommendation Logic (Gemini API)
│ ├── init.py
│ └── recommendtion.py
├── streamlit_app.py # Streamlit application
├── uploads/ # Temporary storage for user uploads (created automatically)
├── outputs/ # Storage for processing results (created automatically)
└── requirements.txt # Python dependencies
```
