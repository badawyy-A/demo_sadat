// src/components/results/BMIDisplay.jsx
import React from 'react';
import { motion } from 'framer-motion';

const BMIDisplay = ({ bmi, category }) => {
  const getBMIColor = () => {
    if (category === 'Underweight') return 'text-blue-500';
    if (category === 'Normal weight') return 'text-green-500';
    if (category === 'Overweight') return 'text-yellow-500';
    if (category === 'Obese') return 'text-red-500';
    return 'text-gray-500';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="card text-center"
    >
      <h2 className="text-2xl font-semibold mb-2">BMI Result</h2>
      <div className="text-5xl font-bold mb-2">{bmi}</div>
      <div className={`text-xl font-medium ${getBMIColor()}`}>
        {category}
      </div>
      <p className="mt-4 text-gray-600 dark:text-gray-400">
        BMI (Body Mass Index) is a measure of body fat based on height and weight.
      </p>
    </motion.div>
  );
};

export default BMIDisplay;