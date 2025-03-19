// src/pages/Results.jsx
import React, { useContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { jsPDF } from 'jspdf';
import { AssessmentContext } from '../context/AssessmentContext';
import ResultsTable from '../components/results/ResultsTable';
import SportRecommendation from '../components/results/SportRecommendation';
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend } from 'chart.js';
import { Radar } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

const Results = () => {
  const { userData, testResults, sportRecommendations, resetAssessment } = useContext(AssessmentContext);
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    console.log("Results component mounted");
    console.log("Test results:", testResults);
    console.log("Sport recommendations:", sportRecommendations);
    
    // Check if we have test results
    const hasTestResults = testResults && Object.keys(testResults).length > 0;
    
    if (!hasTestResults) {
      console.warn("No test results found");
      
      // Wait a moment to see if context updates
      const timer = setTimeout(() => {
        // If after waiting we still don't have results, redirect
        if (!testResults || Object.keys(testResults).length === 0) {
          console.log("No test results after waiting, redirecting to video upload");
          navigate('/video-upload');
        }
      }, 1000);
      
      return () => clearTimeout(timer);
    }

    // Prepare radar chart data
    const testKeys = Object.keys(testResults);
    console.log("Test keys:", testKeys);
    
    if (testKeys.length === 0) {
      console.warn("Test keys length is 0");
      setLoading(false);
      return;
    }
    
    const labels = testKeys.map(key => {
      const testNames = {
        plate_tapping: 'Coordination',
        flamingo_balance: 'Balance',
        curl_up: 'Core Strength',
        push_up: 'Upper Strength',
        cardiovascular: 'Endurance',
        speed: 'Speed',
        pushups: 'Upper Strength',
        curlups: 'Core Strength'
      };
      return testNames[key] || key;
    });

    const data = testKeys.map(key => {
      // Ensure data is a number between 0-100
      const value = Number(testResults[key]);
      return isNaN(value) ? 50 : Math.min(100, Math.max(0, value));
    });

    console.log("Chart labels:", labels);
    console.log("Chart data:", data);

    setChartData({
      labels,
      datasets: [
        {
          label: `${userData?.name || 'Fitness'} Profile`,
          data,
          backgroundColor: 'rgba(59, 130, 246, 0.2)', // Semi-transparent blue fill
          borderColor: 'rgba(59, 130, 246, 1)', // Solid blue border
          borderWidth: 2,
          pointBackgroundColor: 'rgba(59, 130, 246, 1)', // Blue points
          pointBorderColor: '#fff', // White point borders
          pointHoverBackgroundColor: '#fff', // White on hover
          pointHoverBorderColor: 'rgba(59, 130, 246, 1)', // Blue border on hover
          pointRadius: 4, // Larger points for visibility
          pointHoverRadius: 6 // Slightly larger on hover
        },
      ],
    });
    
    setLoading(false);
  }, [testResults, userData, navigate, sportRecommendations]);

  const generatePDF = () => {
    try {
      console.log("Generating PDF");
      const doc = new jsPDF();
      
      // Add title
      doc.setFontSize(20);
      doc.setTextColor(0, 102, 204);
      doc.text('Fitness Assessment Report', 105, 20, { align: 'center' });
      
      // Add candidate details
      doc.setFontSize(12);
      doc.setTextColor(0, 0, 0);
      doc.text(`Name: ${userData?.name || 'Athlete'}`, 20, 40);
      doc.text(`Age: ${userData?.age || 'N/A'} years`, 20, 50);
      doc.text(`Gender: ${userData?.gender ? userData.gender.charAt(0).toUpperCase() + userData.gender.slice(1) : 'Not specified'}`, 20, 60);
      doc.text(`BMI: ${userData?.bmi || 'N/A'}`, 20, 70);
      
      // Add fitness results
      doc.setFontSize(16);
      doc.setTextColor(0, 102, 204);
      doc.text('Fitness Test Results', 20, 90);
      
      doc.setFontSize(10);
      doc.setTextColor(0, 0, 0);
      let yPos = 100;
      
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
      
      if (testResults) {
        Object.keys(testResults).forEach((test, index) => {
          doc.text(`${testNames[test] || test}: ${testResults[test]} / 100`, 20, yPos + (index * 10));
        });
      }
      
      // Add sport recommendations
      doc.setFontSize(16);
      doc.setTextColor(0, 102, 204);
      doc.text('Recommended Sports', 20, 160);
      
      doc.setFontSize(10);
      doc.setTextColor(0, 0, 0);
      
      if (sportRecommendations && sportRecommendations.length > 0) {
        sportRecommendations.forEach((sport, index) => {
          if (sport && sport.name) {
            const compatibility = sport.compatibilityScore 
              ? `${Math.round(sport.compatibilityScore * 100)}%` 
              : 'High';
            doc.text(`${index + 1}. ${sport.name} - Compatibility: ${compatibility}`, 20, 170 + (index * 10));
          }
        });
      } else {
        doc.text("No sport recommendations available", 20, 170);
      }
      
      // Add footer
      doc.setFontSize(8);
      doc.setTextColor(128, 128, 128);
      doc.text('Generated by Fitness Assessment App', 105, 280, { align: 'center' });
      doc.text(`Date: ${new Date().toLocaleDateString()}`, 105, 285, { align: 'center' });
      
      // Save PDF
      const fileName = userData?.name 
        ? `fitness_report_${userData.name.replace(/\s+/g, '_')}.pdf`
        : 'fitness_assessment_report.pdf';
      doc.save(fileName);
      console.log("PDF generated successfully");
    } catch (error) {
      console.error("Error generating PDF:", error);
      alert("Failed to generate PDF. Please try again.");
    }
  };

  // Function to reset assessment data and navigate to home page
  const handleStartNewAssessment = () => {
    console.log("Starting new assessment");
    resetAssessment(); // Clear all assessment data in context
    navigate('/'); // Navigate back to home page
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-DEFAULT mx-auto"></div>
          <p className="mt-4 text-lg">Loading your fitness results...</p>
        </div>
      </div>
    );
  }

  // Fallback if no chart data is available
  if (!chartData) {
    return (
      <div className="max-w-4xl mx-auto text-center py-12">
        <h1 className="text-3xl font-bold mb-6">Results Not Available</h1>
        <p className="text-xl mb-8">
          We couldn't load your fitness assessment results. This might be due to missing data or an error in processing.
        </p>
        <button 
          onClick={() => navigate('/video-upload')} 
          className="btn-primary"
        >
          Return to Video Upload
        </button>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="max-w-4xl mx-auto"
    >
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Assessment Results</h1>
        <button 
          onClick={generatePDF}
          className="btn-primary flex items-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Download PDF
        </button>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <ResultsTable userData={userData} testResults={testResults} />
        
        <div className="card">
          <h2 className="text-2xl font-semibold mb-4">Fitness Profile</h2>
          <div className="h-64">
            <Radar 
              data={chartData} 
              options={{
                scales: {
                  r: {
                    min: 0,
                    max: 100,
                    ticks: {
                      stepSize: 20
                    }
                  }
                },
                elements: {
                  line: {
                    tension: 0.2
                  }
                },
                responsive: true,
                maintainAspectRatio: false
              }}
            />
          </div>
        </div>
      </div>
      
      {sportRecommendations && sportRecommendations.length > 0 ? (
        <SportRecommendation recommendations={sportRecommendations} />
      ) : (
        <div className="card mb-8">
          <h2 className="text-2xl font-semibold mb-4">Sport Recommendations</h2>
          <p>No sport recommendations available at this time.</p>
        </div>
      )}
      
      <div className="mt-8 text-center">
        <button
          onClick={handleStartNewAssessment}
          className="btn-outline"
        >
          Start New Assessment
        </button>
      </div>
    </motion.div>
  );
};

export default Results;