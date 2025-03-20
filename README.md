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
backend/
├── cv_modules/                 # Computer vision processing modules
│   ├── test_videos/            # Sample test videos
│   ├── init.py
│   ├── fitness_tests_age_5_8.py  # Processing fitness tests for ages 5-8
│   ├── fitness_tests_age_9_18.py  # Processing fitness tests for ages 9-18
│   ├── pose_model.py            # Pose estimation model handling
│   ├── process.py               # Core processing logic
│
├── outputs/                     # Stores processed results
│   ├── 5-8_score_result.json
│   ├── scores_results_age5_8.json
│
├── recommendations_module/       # AI-based sport recommendation
│   ├── init.py
│   ├── recommendation.py         # Recommendation logic
│   ├── test.ipynb                # Jupyter notebook for testing
│
├── score_module/                 # Module for handling scores
├── app.py                         # Streamlit application backend
├── main.py                        # Main execution script
├── requirements.txt               # Python dependencies
├── yolo11x-pose.pt                # Pose detection model
├── output_balance_kid4.avi        # Example processed video output

Frontend: Implements the user interface with Streamlit and web technologies.

frontend/
├── public/                       # Public assets
├── src/                          # Source code for frontend
├── index.html                    # Frontend main HTML file
├── Streamlit.py                   # Streamlit UI
├── package.json                   # Frontend dependencies
├── package-lock.json              # Dependency lock file
├── vite.config.js                 # ViteJS configuration
├── tailwind.config.js             # Tailwind CSS config
├── eslint.config.js               # ESLint configuration
├── Dockerfile                     # Docker setup for frontend
├── README.md                      # Frontend documentation
├── .gitignore                     # Git ignore file
├── .env                           # Environment variables
```
## ✅ Installation and Setup

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/badawyy-A/demo_sadat.git
    cd frontend
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate     # On Windows
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Download YOLOv8 Model:**

    Download the `yolo11x-pose.pt` file from the official Ultralytics repository (or a suitable alternative YOLOv8 pose estimation model) and place it in the `cv_modules` directory.  *Provide a link to the official download location here if possible.*  If you use a different model, update the `model_path` in `cv_modules/pose_model.py`.



5.  **Set up the `.env` File:**

    Create a file named `.env` in the root directory of the project.  Add your Gemini API key to this file:

    ```
    GEMINI_API_KEY=your_actual_api_key_here
    ```

    Replace `your_actual_api_key_here` with your actual key.

6.  **Add Reference Data (IMPORTANT):**
    *   Create the files listed above inside `score_module/reference_data/`. Fill them with the proper content.
    *  Create `score_module/score_calculator.py`, and put the classes `Age5to8` and `Age9to18`.

## ▶️ Running the Application

1.  **Activate the Virtual Environment (if you created one):**

    ```bash
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate     # On Windows
    ```

2.  **Run the Streamlit App:**

    ```bash
    streamlit run streamlit_app.py
    ```

    This will start the Streamlit server and open the app in your default web browser.
