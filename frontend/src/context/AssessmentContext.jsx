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

  // Videos state
  const [videos, setVideos] = useState({});

  // Test results state
  const [testResults, setTestResults] = useState({});

  // Sport recommendations state
  const [sportRecommendations, setSportRecommendations] = useState([]);

  // Update user data
  const updateUserData = (data) => {
    setUserData(prevData => ({
      ...prevData,
      ...data
    }));
  };

  // Update user BMI
  const updateUserBMI = (bmi) => {
    setUserData(prevData => ({
      ...prevData,
      bmi
    }));
  };

  // Update videos
  const updateVideos = (newVideos) => {
    setVideos(prevVideos => ({
      ...prevVideos,
      ...newVideos
    }));
  };

  // Update test results
  const updateTestResults = (results) => {
    setTestResults(results);
  };

  // Add or update a video for a specific test type
  const addVideo = (testType, videoFile) => {
    setVideos({ ...videos, [testType]: videoFile });
  };

  // Update sport recommendations
  const updateSportRecommendations = (recommendations) => {
    setSportRecommendations(recommendations);
  };

  // Reset assessment data
  const resetAssessment = () => {
    setUserData({
      name: '',
      age: '',
      gender: '',
      height: '',
      weight: '',
      bmi: '',
      bmiCategory: ''
    });
    setVideos({});
    setTestResults({});
    setSportRecommendations([]);
  };

  return (
    <AssessmentContext.Provider
      value={{
        userData,
        testResults,
        videos,
        sportRecommendations,
        updateUserData,
        updateUserBMI,
        updateVideos,
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