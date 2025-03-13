// src/pages/Home.jsx
import React from 'react';
import { Link } from 'react-router-dom'; // For navigation links
import { motion } from 'framer-motion'; // For animations

const Home = () => {
  return (
    // Main container with centered flex layout
    <div className="flex flex-col items-center">
      
      {/* Animated heading section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center max-w-3xl"
      >
        <h1 className="text-4xl font-bold mb-6">Fitness Assessment & Sport Recommendation</h1>
        <p className="text-xl mb-8">
          A comprehensive tool for coaches to assess young athletes and recommend suitable sports
          based on their physical abilities.
        </p>
      </motion.div>

      {/* Animated "How It Works" card */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5, duration: 1.5 }}
        className="card w-full max-w-3xl mb-8"
      >
        <h2 className="text-2xl font-semibold mb-4">How It Works</h2>
        <ol className="list-decimal list-inside space-y-4 pl-4">
          <li className="text-lg">
            <span className="font-medium">Enter candidate details</span> - 
            Provide basic information like age, gender, weight, and height.
          </li>
          <li className="text-lg">
            <span className="font-medium">Upload fitness test videos</span> - 
            Based on the age group, upload videos for various fitness tests.
          </li>
          <li className="text-lg">
            <span className="font-medium">AI analysis</span> - 
            Our system analyzes the videos and calculates performance scores.
          </li>
          <li className="text-lg">
            <span className="font-medium">Get recommendations</span> - 
            Receive sport recommendations based on the candidate's fitness profile.
          </li>
        </ol>
      </motion.div>

      {/* Animated "Get Started" button */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.5, duration: 0.8 }}
        className="text-center"
      >
        <Link to="/user-input" className="btn-primary text-lg px-8 py-3">
          Get Started
        </Link>
      </motion.div>
    </div>
  );
};

export default Home;