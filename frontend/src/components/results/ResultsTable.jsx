// src/components/results/ResultsTable.jsx
import React from 'react';

const ResultsTable = ({ userData, testResults }) => {
  // Define test name mapping
  const testNames = {
    plate_tapping: 'Coordination (Plate Tapping)',
    flamingo_balance: 'Balance (Flamingo Test)',
    curl_up: 'Core Strength (Curl-up)',
    push_up: 'Upper Body Strength (Push-up)',
    cardiovascular: 'Cardiovascular Endurance',
    speed: 'Speed',
    pushups: 'Upper Body Strength (Push-up)',
    curlups: 'Core Strength (Curl-up)'
  };

  // Define level descriptions
  const levelDescriptions = {
    'L1': 'Work Harder',
    'L2': 'Must Improve',
    'L3': 'Can do Better',
    'L4': 'Good',
    'L5': 'Very Good',
    'L6': 'Athletic',
    'L7': 'Sports Fit'
  };

  // Get color based on level
  const getLevelColor = (level) => {
    const colors = {
      'L1': 'bg-red-500',
      'L2': 'bg-orange-500',
      'L3': 'bg-yellow-500',
      'L4': 'bg-blue-400',
      'L5': 'bg-blue-500',
      'L6': 'bg-green-400',
      'L7': 'bg-green-500'
    };
    return colors[level] || 'bg-gray-500';
  };

  // Process test results to handle the API format
  const processedResults = React.useMemo(() => {
    const processed = {};
    Object.entries(testResults || {}).forEach(([key, value]) => {
      if (typeof value === 'object' && value !== null) {
        // If it's an object with score and level properties from the API
        processed[key] = {
          score: value.score || 0,
          displayScore: value.score * 10, // Convert to 0-100 scale for display
          level: value.level || 'N/A'
        };
      } else if (typeof value === 'number') {
        // If it's a direct number (legacy format)
        // Estimate the level based on score
        let level = 'L1';
        const numericScore = value / 10; // Convert back to 0-10 scale
        if (numericScore >= 10) level = 'L7';
        else if (numericScore >= 9) level = 'L6';
        else if (numericScore >= 8) level = 'L5';
        else if (numericScore >= 7) level = 'L4';
        else if (numericScore >= 6) level = 'L3';
        else if (numericScore >= 4) level = 'L2';
        
        processed[key] = {
          score: numericScore,
          displayScore: value,
          level: level
        };
      }
    });
    return processed;
  }, [testResults]);

  return (
    <div className="card">
      <h2 className="text-2xl font-semibold mb-4">Fitness Test Results</h2>
      
      <div className="mb-4">
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <p className="text-gray-600 dark:text-gray-400">Name</p>
            <p className="font-medium">{userData.name || 'Athlete'}</p>
          </div>
          <div>
            <p className="text-gray-600 dark:text-gray-400">Age</p>
            <p className="font-medium">{userData.age} years</p>
          </div>
          <div>
            <p className="text-gray-600 dark:text-gray-400">Gender</p>
            <p className="font-medium">
              {userData.gender 
                ? userData.gender.charAt(0).toUpperCase() + userData.gender.slice(1) 
                : 'Not specified'}
            </p>
          </div>
          <div>
            <p className="text-gray-600 dark:text-gray-400">BMI</p>
            <p className="font-medium">
              {userData.bmi 
                ? parseFloat(userData.bmi).toFixed(1) 
                : 'N/A'}
            </p>
          </div>
        </div>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b">
              <th className="text-left py-2">Test</th>
              <th className="text-center py-2">Score</th>
              <th className="text-center py-2">Level</th>
              <th className="text-right py-2">Performance</th>
            </tr>
          </thead>
          <tbody>
            {Object.keys(processedResults).map(test => {
              const result = processedResults[test];
              const levelColor = getLevelColor(result.level);
              
              return (
                <tr key={test} className="border-b">
                  <td className="py-2">{testNames[test] || test}</td>
                  <td className="text-center py-2">{result.displayScore}</td>
                  <td className="text-center py-2">
                    <span className={`${levelColor} text-white px-2 py-1 rounded text-xs`}>
                      {result.level}
                    </span>
                  </td>
                  <td className="py-2 text-right">
                    <span className="text-sm">
                      {levelDescriptions[result.level] || 'Unknown'}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      
      <div className="mt-4 p-4 bg-gray-100 dark:bg-gray-800 rounded-lg">
        <h3 className="font-medium mb-2">Fitness Assessment Levels</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
          <div><span className="inline-block w-3 h-3 bg-red-500 rounded-full mr-1"></span> L1: Work Harder</div>
          <div><span className="inline-block w-3 h-3 bg-orange-500 rounded-full mr-1"></span> L2: Must Improve</div>
          <div><span className="inline-block w-3 h-3 bg-yellow-500 rounded-full mr-1"></span> L3: Can do Better</div>
          <div><span className="inline-block w-3 h-3 bg-blue-400 rounded-full mr-1"></span> L4: Good</div>
          <div><span className="inline-block w-3 h-3 bg-blue-500 rounded-full mr-1"></span> L5: Very Good</div>
          <div><span className="inline-block w-3 h-3 bg-green-400 rounded-full mr-1"></span> L6: Athletic</div>
          <div><span className="inline-block w-3 h-3 bg-green-500 rounded-full mr-1"></span> L7: Sports Fit</div>
        </div>
      </div>
    </div>
  );
};

export default ResultsTable;