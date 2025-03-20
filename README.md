# Fitness Assessment and Sport Recommendation System

## 📌 Project Overview

This project is a comprehensive **Fitness Assessment and Sport Recommendation System** designed to evaluate candidates' fitness levels (ages 5-18) and suggest suitable sports based on their performance.  It leverages **computer vision** for automated video analysis of fitness tests and an **AI-powered recommendation engine** (using Google's Gemini API) to provide personalized sport suggestions. The system is built with a modular backend (Python) and an interactive frontend (Streamlit and React.js).

## 🚀 Features

*   **Automated Fitness Assessment:**  Analyzes video recordings of standardized fitness tests using YOLOv8 pose estimation.
*   **Age-Specific Tests:** Supports different tests for two age groups:
    *   **Ages 5-8:** Plate Tapping (coordination) and Flamingo Balance Test.
    *   **Ages 9-18:** Push-ups, Curl-ups, 600m Run/Walk, and 50m Dash.
*   **AI-Powered Recommendations:**  Uses Google's Gemini API to generate personalized sport recommendations based on the assessed fitness attributes and a knowledge base of sport requirements.
*   **User-Friendly Interface:**  A modern React web application provides an intuitive interface for:
    *   Entering candidate details (age, gender, weight, height).
    *   Uploading video recordings of fitness tests.
    *   Viewing calculated scores and performance levels.
    *   Receiving top 3 sport recommendations.
*   **BMI Calculation:** Automatically calculates and displays the candidate's Body Mass Index (BMI).
*   **Modular Design:**  Well-structured code with separate modules for computer vision, scoring, recommendations, and the React UI, making it easy to maintain and extend.
*   **JSON Output:**  Saves intermediate results (CV analysis and scores) to JSON files for further analysis or integration with other systems.

## 📊 Usage (Workflow)

1.  **Candidate Information:** The user (e.g., a coach) enters the candidate's age, gender, weight, and height.
2.  **Video Upload:** Based on the candidate's age, the user is prompted to upload the appropriate video recordings of the required fitness tests.
3.  **Automated Analysis:** The system processes the uploaded videos using YOLOv8 pose estimation to extract relevant performance metrics (e.g., repetitions, time, balance errors).
4.  **Scoring:** The extracted metrics are compared against age- and gender-specific benchmarks (currently using *placeholder* data – **see Important Notes below**) to determine performance levels and scores.
5.  **Recommendation Generation:**  The calculated scores, along with the candidate's information, are sent to the Gemini API, which provides a ranked list of the top 3 recommended sports.
6.  **Results Display:** The React app displays the calculated BMI, individual test scores, performance levels, and the top 3 recommended sports.

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
    *   React.js
    *   Vite
    *   Tailwind CSS
    *   ESLint
    *   PostCSS
* **Dependencies Management:** package.json and requirements.txt

## 📂 Project Structure
```
fitness_app/
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
├── app.py                         # API endpoints
├── main.py                        # Main execution script
├── requirements.txt               # Python dependencies
├── yolo11x-pose.pt                # Pose detection model
├── output_balance_kid4.avi        # Example processed video output

frontend/
├── node_modules/       # Project dependencies
├── public/             # Static files served as-is
├── src/                # Source code
│   ├── api/            # API client and endpoints
│   ├── assets/         # Static assets (images, fonts, etc.)
│   ├── components/     # Reusable UI components
│   ├── context/        # React context providers
│   ├── data/           # Data fetching and state management
│   ├── pages/          # Page components
│   ├── styles/         # CSS and styling files
│   ├── utils/          # Utility functions and helpers
│   ├── App.jsx         # Main application component
│   └── main.jsx        # Application entry point
├── .gitignore          # Git ignore file
├── eslint.config.js    # ESLint configuration
├── index.html          # HTML entry point
├── package-lock.json   # Locked dependencies
├── package.json        # Project metadata and dependencies
├── postcss.config.js   # PostCSS configuration
├── README.md           # Frontend documentation
├── tailwind.config.js  # Tailwind CSS configuration
├── vite.config.js      # Vite configuration
├── Dockerfile          # Docker setup for frontend
├── .env                # Environment variables
```

## ✅ Installation and Setup

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/badawyy-A/demo_sadat.git
    ```

2.  **Backend Setup:**

    ```bash
    cd backend
    
    # Create a Virtual Environment (Recommended)
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate     # On Windows
    
    # Install Dependencies
    pip install -r requirements.txt
    ```

3.  **Download YOLOv8 Model:**

    Download the `yolo11x-pose.pt` file from the official Ultralytics repository (or a suitable alternative YOLOv8 pose estimation model) and place it in the `cv_modules` directory.  *Provide a link to the official download location here if possible.*  If you use a different model, update the `model_path` in `cv_modules/pose_model.py`.

4.  **Backend Environment Setup:**

    Create a file named `.env` in the backend directory.  Add your Gemini API key to this file:

    ```
    GEMINI_API_KEY=your_actual_api_key_here
    ```

    Replace `your_actual_api_key_here` with your actual key.

5. **Add Reference Data (IMPORTANT):**
    *   Create the files listed above inside `score_module/reference_data/`. Fill them with the proper content.
    *  Create `score_module/score_calculator.py`, and put the classes `Age5to8` and `Age9to18`.

6.  **Frontend Setup:**

    ```bash
    cd ../frontend
    
    # Install Dependencies
    npm install
    # or
    yarn
    ```

7.  **Frontend Environment Setup:**

    Create a file named `.env` in the frontend directory. Add your API endpoint:

    ```
    VITE_API_URL=http://localhost:5000/api
    ```

## ▶️ Running the Application

1.  **Start the Backend:**

    ```bash
    cd backend
    
    # Activate the Virtual Environment (if you created one)
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate     # On Windows
    
    # Run the Backend Server
    python app.py
    ```

    This will start the backend server, typically at `http://localhost:5000`.

2.  **Start the Frontend:**

    ```bash
    cd frontend
    
    # Run the Development Server
    npm run dev
    # or
    yarn dev
    ```

    The React application will be available at `http://localhost:5173` by default.

## 🏃‍♀️ Development

- **Backend Development:**
  Make changes to the Python files and restart the server as needed.

- **Frontend Development:**
  The Vite development server includes hot module replacement, so changes will appear immediately.

## 🛠️ Building for Production

1.  **Backend Production:**
    Configure your production server (e.g., Gunicorn, uWSGI) according to your deployment environment.

2.  **Frontend Production Build:**

    ```bash
    cd frontend
    
    npm run build
    # or
    yarn build
    ```

    The built files will be in the `dist` directory and can be served by any static file server.

## 🚢 Docker

This project includes Dockerfiles for both frontend and backend containerization.

**Build and Run Frontend:**
```bash
cd frontend
docker build -t frontend-app .
docker run -p 8080:80 frontend-app
```

The frontend will be available at `http://localhost:8080`.

**Build and Run Backend:**
```bash
cd backend
docker build -t backend-app .
docker run -p 5000:5000 backend-app
```

The backend will be available at `http://localhost:5000`.

## 📚 Tech Stack

- **Backend:**
  - Python
  - OpenCV
  - YOLOv8
  - LangChain
  - Google Gemini API

- **Frontend:**
  - [React](https://reactjs.org/)
  - [Vite](https://vitejs.dev/)
  - [Tailwind CSS](https://tailwindcss.com/)
  - [ESLint](https://eslint.org/)
  - [PostCSS](https://postcss.org/)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
