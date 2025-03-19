// src/components/results/ResultsTable.jsx
import React from 'react';
import { motion } from 'framer-motion';

const ResultsTable = ({ userData, testResults }) => {
  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-500';
    if (score >= 70) return 'text-blue-500';
    if (score >= 60) return 'text-yellow-500';
    return 'text-red-500';
  };

  const getScoreLabel = (score) => {
    if (score >= 80) return 'Excellent';
    if (score >= 70) return 'Good';
    if (score >= 60) return 'Average';
    return 'Needs Improvement';
  };

  const formatTestName = (testKey) => {
    const testNames = {
      coordination: 'Coordination',
      balance: 'Balance',
      curl_up: 'Curl-up',
      push_up: "Push-up",
      cardiovascular: 'Cardiovascular Endurance',
      speed: 'Speed'
    };
    return testNames[testKey] || testKey;
  };

  const tests = Object.keys(testResults).filter(key => testResults[key] !== null);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="card"
    >
      <h2 className="text-2xl font-semibold mb-4">Fitness Assessment Results</h2>
      
      <div className="mb-4 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-3 bg-gray-100 dark:bg-gray-800 rounded-lg">
          <div className="text-sm text-gray-500 dark:text-gray-400">Name</div>
          <div className="font-medium">{userData.name}</div>
        </div>
        <div className="p-3 bg-gray-100 dark:bg-gray-800 rounded-lg">
          <div className="text-sm text-gray-500 dark:text-gray-400">Age & Gender</div>
          <div className="font-medium">{userData.age} years, {userData.gender.charAt(0).toUpperCase() + userData.gender.slice(1)}</div>
        </div>
        <div className="p-3 bg-gray-100 dark:bg-gray-800 rounded-lg">
          <div className="text-sm text-gray-500 dark:text-gray-400">BMI</div>
          <div className="font-medium">{userData.bmi} ({userData.bmiCategory})</div>
        </div>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-gray-100 dark:bg-gray-800">
              <th className="p-3 text-left">Fitness Component</th>
              <th className="p-3 text-center">Score</th>
              <th className="p-3 text-center">Performance</th>
            </tr>
          </thead>
          <tbody>
            {tests.map(test => (
              <tr key={test} className="border-t border-gray-200 dark:border-gray-700">
                <td className="p-3 font-medium">{formatTestName(test)}</td>
                <td className="p-3 text-center">{testResults[test]}</td>
                <td className={`p-3 text-center ${getScoreColor(testResults[test])}`}>
                  {getScoreLabel(testResults[test])}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </motion.div>
  );
};

export default ResultsTable;

