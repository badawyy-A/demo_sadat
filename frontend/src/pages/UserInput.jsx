import React, { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { AssessmentContext } from '../context/AssessmentContext';
import { calculateBMI, getBMICategory } from '../utils/bmiCalculator';
import BMIDisplay from '../components/results/BMIDisplay';
import { sendUserInput } from '../service/api';

const UserInput = () => {
  const { userData, updateUserData } = useContext(AssessmentContext);
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null); // Stores success/error message

  // Handle input changes and update the state
  const handleChange = (e) => {
    const { name, value } = e.target;
    updateUserData({ [name]: value });
  };

  // Handle BMI Calculation and API request
  const handleCalculateBMI = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null); // Clear previous messages

    try {
      // Calculate BMI and determine category
      const bmi = calculateBMI(parseFloat(userData.weight), parseFloat(userData.height));
      const bmiCategory = getBMICategory(bmi, parseInt(userData.age), userData.gender);

      updateUserData({ bmi, bmiCategory });

      // Send user data to backend API
      const response = await sendUserInput({
        age: userData.age,
        gender: userData.gender,
        weight: userData.weight,
        height: userData.height,
      });

      // Display success message
      setMessage({ type: 'success', text: `Success: ${response.message}` });
    } catch (err) {
      // Display error message
      setMessage({ type: 'error', text: 'Failed to send user data. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  
  const handleContinue = () => {
    // Navigate to video upload page
    navigate('/video-upload');
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1 }}
      className="max-w-2xl mx-auto"
    >
      <h1 className="text-3xl font-bold mb-6">Candidate Details</h1>

      <div className="card mb-8">
        <form onSubmit={handleCalculateBMI}>
          {/* Full Name Field */}
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

          {/* Age and Gender Fields */}
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

          {/* Weight and Height Fields */}
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

          {/* Submit Button */}
          <div className="mt-6">
            <button type="submit" className="btn-primary w-full" disabled={loading}>
              {loading ? 'Submitting...' : 'Calculate BMI'}
            </button>
          </div>

          {/* Display Success/Error Message */}
          {message && (
            <p className={`mt-4 p-2 rounded text-center ${message.type === 'success' ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'}`}>
              {message.text}
            </p>
          )}
        </form>
      </div>

      {/* BMI Display & Continue Button */}
      {userData.bmi && (
        <>
          <BMIDisplay bmi={userData.bmi} category={userData.bmiCategory} />
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

export default UserInput;
