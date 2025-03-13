// src/pages/Analysis.jsx
import React, { useContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { AssessmentContext } from '../context/AssessmentContext';

// Mock functions for video analysis - in a real app these would call backend APIs
const analyzeVideo = (videoFile, testType, userData) => {
  return new Promise((resolve) => {
    // Simulate API delay
    setTimeout(() => {
      // Mock results based on test type
      let score;
      const gender = userData.gender;
      const age = parseInt(userData.age);
      
      // Generate random score based on gender and age
      // In a real app, this would be determined by AI video analysis
      if (testType === 'coordination') {
        score = Math.floor(Math.random() * 20) + 70; // 70-90
      } else if (testType === 'balance') {
        score = Math.floor(Math.random() * 25) + 65; // 65-90
      } else if (testType === 'muscularStrength') {
        score = gender === 'male' ? 
          Math.floor(Math.random() * 20) + 70 : 
          Math.floor(Math.random() * 20) + 65;
      } else if (testType === 'flexibility') {
        score = gender === 'female' ? 
          Math.floor(Math.random() * 20) + 75 : 
          Math.floor(Math.random() * 20) + 65;
      } else if (testType === 'cardiovascular') {
        score = Math.floor(Math.random() * 30) + 60; // 60-90
      } else if (testType === 'speed') {
        score = Math.floor(Math.random() * 25) + 65; // 65-90
      }
      
      resolve(score);
}, 1500); // 1.5 seconds delay to simulate processing
});
};

const Analysis = () => {
const { userData, videos, updateTestResults } = useContext(AssessmentContext);
const [progress, setProgress] = useState(0);
const [currentTest, setCurrentTest] = useState('');
const [processing, setProcessing] = useState(true);
const navigate = useNavigate();

useEffect(() => {
  // Redirect if no videos
  if (Object.keys(videos).length === 0) {
    navigate('/video-upload');
    return;
  }

  const analyzeAllVideos = async () => {
    const testResults = {};
    const testTypes = Object.keys(videos).filter(key => videos[key]);
    const totalTests = testTypes.length;
    
    for (let i = 0; i < testTypes.length; i++) {
      const testType = testTypes[i];
      setCurrentTest(testType);

      // Simulate gradual progress increase for this test
      const startProgress = (i / totalTests) * 100;
      const endProgress = ((i + 1) / totalTests) * 100;
      const steps = 20; // Number of steps for smooth progress
      const increment = (endProgress - startProgress) / steps;
      for (let step = 0; step <= steps; step++) {
        setProgress(startProgress + (increment * step));
        await new Promise(resolve => setTimeout(resolve, 75)); // Small delay for smooth animation
      }

      // Analyze video
      const score = await analyzeVideo(videos[testType], testType, userData);
      testResults[testType] = score;
    }

    // Update test results in context
    updateTestResults(testResults);
    setProcessing(false);

    // Auto-navigate after a short delay
    setTimeout(() => {
      navigate('/results');
    }, 1500);
  };

  analyzeAllVideos();
}, [videos, userData, updateTestResults, navigate]);

const getTestName = (testType) => {
  const testNames = {
    coordination: 'Coordination (Plate Tapping Test)',
    balance: 'Balance (Flamingo Balance Test)',
    muscularStrength: 'Muscular Strength (Curl-up and Push-up)',
    flexibility: 'Flexibility (Sit and Reach Test)',
    cardiovascular: 'Cardiovascular Endurance (600m Run/Walk)',
    speed: 'Speed (50m Dash)'
  };
  return testNames[testType] || testType;
};

return (
  <motion.div
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    transition={{ duration: 1 }}
    className="max-w-3xl mx-auto text-center"
  >
    <h1 className="text-3xl font-bold mb-8">Analyzing Videos</h1>

    <div className="card mb-8">
      {processing ? (
        <>
          <div className="mb-4">
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-4 mb-2">
              <div 
                className="bg-primary-DEFAULT h-4 rounded-full transition-all duration-300 ease-out"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {Math.round(progress)}% complete
            </p>
          </div>

          <p className="text-xl font-medium mb-4">
            Analyzing: {getTestName(currentTest)}
          </p>
          <p className="text-gray-600 dark:text-gray-400">
            Our AI is processing the video to extract performance metrics...
          </p>
        </>
      ) : (
        <>
          <div className="text-5xl text-green-500 mb-4">✓</div>
          <h2 className="text-2xl font-semibold mb-4">Analysis Complete!</h2>
          <p className="text-lg">
            Redirecting to results page...
          </p>
        </>
      )}
    </div>
  </motion.div>
);
};

export default Analysis;