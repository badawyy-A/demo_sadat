// src/pages/VideoUpload.jsx
import React, { useContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { AssessmentContext } from '../context/AssessmentContext'; // Context for user data and videos
import { uploadVideos } from '../service/api'; // Import the API function

const VideoUpload = () => {
  const { userData, videos, addVideo } = useContext(AssessmentContext); // Access context data
  const [ageGroup, setAgeGroup] = useState(null); // State for age group
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // Hook for navigation

  // Determine age group based on user age
  useEffect(() => {
    if (!userData.age) {
      navigate('/user-input'); // Redirect if no user data
      return;
    }
    
    const age = parseInt(userData.age);
    if (age >= 5 && age <= 8) {
      setAgeGroup('junior');
    } else if (age >= 9 && age <= 18) {
      setAgeGroup('senior');
    }
  }, [userData.age, navigate]);

  // Define tests for junior age group
  const juniorTests = [
    { id: 'coordination', name: 'Coordination', description: 'Plate Tapping Test' },
    { id: 'balance', name: 'Balance', description: 'Flamingo Balance Test' }
  ];

  // Define tests for senior age group
  const seniorTests = [
    { id: 'curl_up', name: 'Curl-up', description: 'Curl-up' },
    { id: 'push_up', name: 'Push-up', description: 'Push-up' },
    { id: 'cardiovascular', name: 'Cardiovascular Endurance', description: '600m Run/Walk Test' },
    { id: 'speed', name: 'Speed', description: '50m Dash Test' }
  ];

  // Handle file selection for video upload
  const handleFileChange = (testId, e) => {
    if (e.target.files && e.target.files[0]) {
      addVideo(testId, e.target.files[0]); // Add video to context
    }
  };

  // Handle form submission to navigate to analysis
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      // Determine the appropriate age range format for the API
      const apiAgeRange = ageGroup === 'junior' ? '5-8' : '9-18';
      
      // Call the API function to upload videos
      await uploadVideos(apiAgeRange, videos);
      
      // If successful, navigate to analysis page
      navigate('/analysis');
    } catch (err) {
      // Display error message to the user
      setError(err.response?.data?.detail || 'Failed to upload videos. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Show loading state if age group not determined
  if (!ageGroup) {
    return <div className="text-center py-12">Loading...</div>;
  }

  // Select tests based on age group
  const testsToDisplay = ageGroup === 'junior' ? juniorTests : seniorTests;

  return (
    // Animated container for video upload form
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1 }}
      className="max-w-3xl mx-auto"
    >
      <h1 className="text-3xl font-bold mb-2">Upload Test Videos</h1>
      <p className="text-gray-600 dark:text-gray-400 mb-6">
        Based on {userData.name}'s age ({userData.age} years), please upload videos for the following tests:
      </p>

      {/* Display error message if there's an error */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <strong>Error:</strong> {error}
        </div>
      )}
      {/* Form card for video uploads */}
      <div className="card mb-8">
        <form onSubmit={handleSubmit}>
          <div className="space-y-6">
            {testsToDisplay.map((test) => (
              // Render each test with upload field
              <div key={test.id} className="p-4 border rounded-lg border-gray-200 dark:border-gray-700">
                <h3 className="text-xl font-medium mb-2">{test.name}</h3>
                <p className="text-gray-600 dark:text-gray-400 mb-4">{test.description}</p>

                {/* File input for video upload */}
                <div className="flex items-center space-x-4">
                  <div className="flex-grow">
                    <label 
                      htmlFor={`video-${test.id}`} 
                      className="block w-full p-3 text-center border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800"
                    >
                      {videos[test.id] ? videos[test.id].name : 'Select Video File'}
                    </label>
                    <input
                      type="file"
                      id={`video-${test.id}`}
                      accept="video/*"
                      className="hidden"
                      onChange={(e) => handleFileChange(test.id, e)}
                    />
                  </div>

                  {/* Remove button for uploaded video */}
                  {videos[test.id] && (
                    <button
                      type="button"
                      onClick={() => addVideo(test.id, null)}
                      className="text-red-500 hover:text-red-700"
                    >
                      Remove
                    </button>
                  )}
                </div>

                {/* Display selected video name */}
                {videos[test.id] && (
                  <div className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                    Video selected: {videos[test.id].name}
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Navigation buttons */}
          <div className="mt-8 flex justify-between">
            <button
              type="button"
              onClick={() => navigate('/user-input')}
              className="btn-outline"
            >
              Back
            </button>
            <button
              type="submit"
              className="btn-primary"
              disabled={Object.keys(videos).length === 0 || loading}
            >
              {loading ? 'Uploading...' : 'Analyze Videos'}
            </button>
          </div>
        </form>
      </div>
    </motion.div>
  );
};

export default VideoUpload; // Export the component