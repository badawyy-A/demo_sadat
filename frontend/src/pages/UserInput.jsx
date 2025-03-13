// src/pages/UserInput.jsx
import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom'; // For navigation
import { motion } from 'framer-motion'; // For animations
import { AssessmentContext } from '../context/AssessmentContext'; // Context for user data
import { calculateBMI, getBMICategory } from '../utils/bmiCalculator'; // BMI utilities
import BMIDisplay from '../components/results/BMIDisplay'; // Component to display BMI

const UserInput = () => {
  const { userData, updateUserData } = useContext(AssessmentContext); // Access user data context
  const navigate = useNavigate(); // Hook for navigation

  // Handle form input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    updateUserData({ [name]: value });
  };

  // Handle BMI calculation
  const handleCalculateBMI = (e) => {
    e.preventDefault();
    // Calculate BMI and category
    const bmi = calculateBMI(parseFloat(userData.weight), parseFloat(userData.height));
    const bmiCategory = getBMICategory(bmi, parseInt(userData.age), userData.gender);
    // Update context with BMI data
    updateUserData({ bmi, bmiCategory });
  };

  // Handle navigation to the next page
  const handleContinue = () => {
    // Navigate to video upload page
    navigate('/video-upload');
  };

  return (
    // Animated container for form
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1 }}
      className="max-w-2xl mx-auto"
    >
      <h1 className="text-3xl font-bold mb-6">Candidate Details</h1>

      {/* Form card */}
      <div className="card mb-8">
        <form onSubmit={handleCalculateBMI}>
          {/* Full Name input */}
          <div className="form-group">
            <label htmlFor="name" className="form-label">Full Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={userData.name}
              onChange={handleChange}
              className="form-input"
              required
            />
          </div>

          {/* Age and Gender inputs */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="form-group">
              <label htmlFor="age" className="form-label">Age (5-18 years)</label>
              <input
                type="number"
                id="age"
                name="age"
                min="5"
                max="18"
                value={userData.age}
                onChange={handleChange}
                className="form-input"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="gender" className="form-label">Gender</label>
              <select
                id="gender"
                name="gender"
                value={userData.gender}
                onChange={handleChange}
                className="form-input"
                required
              >
                <option value="">Select Gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
              </select>
            </div>
          </div>

          {/* Weight and Height inputs */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="form-group">
              <label htmlFor="weight" className="form-label">Weight (kg)</label>
              <input
                type="number"
                id="weight"
                name="weight"
                min="10"
                max="150"
                step="0.1"
                value={userData.weight}
                onChange={handleChange}
                className="form-input"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="height" className="form-label">Height (cm)</label>
              <input
                type="number"
                id="height"
                name="height"
                min="70"
                max="220"
                step="0.1"
                value={userData.height}
                onChange={handleChange}
                className="form-input"
                required
              />
            </div>
          </div>

          {/* Button to calculate BMI */}
          <div className="mt-6">
            <button type="submit" className="btn-primary w-full">
              Calculate BMI
            </button>
          </div>
        </form>
      </div>

      {/* Display BMI results if calculated */}
      {userData.bmi && (
        <>
          <BMIDisplay bmi={userData.bmi} category={userData.bmiCategory} />
          {/* Button to continue to the next page */}
          <div className="mt-6">
            <button onClick={handleContinue} className="btn-primary w-full">
              Continue
            </button>
          </div>
        </>
      )}
    </motion.div>
  );
};

export default UserInput; // Export the component