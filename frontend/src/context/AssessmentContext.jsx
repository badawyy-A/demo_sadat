// src/context/AssessmentContext.jsx
import React, { createContext, useState } from 'react';

// Create a context for managing assessment-related data
export const AssessmentContext = createContext();

// Provider component to wrap the app and manage assessment state
export const AssessmentProvider = ({ children }) => {
  // State for user data (candidate details)
  const [userData, setUserData] = useState({
    name: '',
    age: '',
    gender: '',
    weight: '',
    height: '',
    bmi: null,
    bmiCategory: ''
  });

  // State for test results (fitness scores)
  const [testResults, setTestResults] = useState({
    coordination: null,
    balance: null,
    curl_up: null,
    push_up: null,
    cardiovascular: null,
    speed: null
  });

  // State for uploaded videos
  const [videos, setVideos] = useState({});

  // State for sport recommendations
  const [sportRecommendations, setSportRecommendations] = useState([]);

  // Update user data with new values
  const updateUserData = (data) => {
    setUserData({ ...userData, ...data });
  };

  // Update test results with new values
  const updateTestResults = (results) => {
    setTestResults({ ...testResults, ...results });
  };

  // Add or update a video for a specific test type
  const addVideo = (testType, videoFile) => {
    setVideos({ ...videos, [testType]: videoFile });
  };

  // Update sport recommendations
  const updateSportRecommendations = (recommendations) => {
    setSportRecommendations(recommendations);
  };

  // Reset all assessment data to initial state
  const resetAssessment = () => {
    setUserData({
      name: '',
      age: '',
      gender: '',
      weight: '',
      height: '',
      bmi: null,
      bmiCategory: ''
    });
    setTestResults({
      coordination: null,
      balance: null,
      curl_up: null,
      push_up: null,
      cardiovascular: null,
      speed: null
    });
    setVideos({});
    setSportRecommendations([]);
  };

  // Provide context values to children
  return (
    <AssessmentContext.Provider
      value={{
        userData,
        testResults,
        videos,
        sportRecommendations,
        updateUserData,
        updateTestResults,
        addVideo,
        updateSportRecommendations,
        resetAssessment
      }}
    >
      {children}
    </AssessmentContext.Provider>
  );
};