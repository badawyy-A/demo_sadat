import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

const Home = () => {
  // State to track the currently active feature in the carousel
  const [activeFeature, setActiveFeature] = useState(0);

  // Array of key features displayed in the carousel
  const features = [
    {
      icon: "👤",
      title: "Comprehensive Athlete Profiling",
      description: "Easily input key candidate data, including Age (5-18 years), Gender, Weight, and Height."
    },
    {
      icon: "📊",
      title: "Advanced BMI Calculation",
      description: "Instantly computes Body Mass Index (BMI) to evaluate baseline fitness levels."
    },
    {
      icon: "🎥",
      title: "AI-Powered Performance Analysis",
      description: "Upload and analyze videos of various fitness assessments based on age categories."
    },
    {
      icon: "📈",
      title: "Automated Performance Benchmarking",
      description: "Leverages AI-driven algorithms to extract key performance metrics and compare results against scientifically validated standards."
    },
    {
      icon: "📋",
      title: "In-Depth Results Table",
      description: "Presents a detailed breakdown of each athlete's fitness parameters, performance scores, and recommended sport."
    },
    {
      icon: "🏆",
      title: "Intelligent Sport-Specific Recommendations",
      description: "Utilizes an open-source LLM to identify and suggest the top three sports best aligned with each candidate's unique fitness attributes."
    },
    {
      icon: "📄",
      title: "Downloadable Professional Reports",
      description: "Generate, review, and share detailed fitness assessment reports in PDF format, enhancing decision-making and athlete development strategies."
    }
  ];

  // Automatically switch features every 4 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setActiveFeature((prev) => (prev + 1) % features.length);
    }, 5000);
    return () => clearInterval(interval);
  }, [features.length]);

  // Animation variants for different sections
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1,
      transition: { 
        staggerChildren: 0.2,
        delayChildren: 0.3
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  const featureVariants = {
    hidden: { opacity: 0, scale: 0.8 },
    visible: { opacity: 1, scale: 1, transition: { duration: 0.5 } }
  };

  return (
    <motion.div 
      className="max-w-4xl mx-auto px-4 py-8"
      initial="hidden"
      animate="visible"
      variants={containerVariants}
    >
      {/* Hero Section */}
      <motion.div className="text-center mb-16" variants={itemVariants}>
        <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">ESTADAT PROJECT</h1>
        <motion.div 
          className="h-1 w-24 bg-gradient-to-r from-blue-600 to-purple-600 mx-auto mb-6"
          initial={{ width: 0 }}
          animate={{ width: "6rem" }}
          transition={{ delay: 0.5, duration: 0.8 }}
        />
        <h2 className="text-2xl md:text-3xl font-semibold mb-6">AI-Powered Fitness Assessment & Sport Recommendation</h2>
        <p className="text-lg text-gray-700 dark:text-gray-300 mb-8">
          Revolutionizing Fitness Evaluations with Cutting-Edge AI
        </p>
      </motion.div>

      {/* Description */}
      <motion.div 
        className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-12"
        variants={itemVariants}
      >
        <p className="text-lg leading-relaxed">
          Estadat is a cutting-edge state-of-the-art platform designed for professional fitness coaches 
          to accurately assess young athletes' physical capabilities and recommend the most suitable sports for them. 
          By integrating AI-powered video analysis and precise biometric calculations, Estadat delivers actionable 
          insights to enhance athletic development and performance optimization.
        </p>
      </motion.div>

      {/* Age Categories Section */}
      <motion.div variants={itemVariants} className="mb-12">
        <h3 className="text-xl font-bold mb-4">Age-Specific Assessment Categories:</h3>
        <div className="grid md:grid-cols-2 gap-6">
          <motion.div 
            className="bg-blue-50 dark:bg-blue-900/30 p-6 rounded-lg border border-blue-200 dark:border-blue-800"
            whileHover={{ scale: 1.03 }}
            transition={{ type: "spring", stiffness: 300 }}
          >
            <h4 className="text-lg font-semibold mb-2">Ages 5-8</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>Coordination Tests</li>
              <li>Balance Tests</li>
            </ul>
          </motion.div>
          <motion.div 
            className="bg-purple-50 dark:bg-purple-900/30 p-6 rounded-lg border border-purple-200 dark:border-purple-800"
            whileHover={{ scale: 1.03 }}
            transition={{ type: "spring", stiffness: 300 }}
          >
            <h4 className="text-lg font-semibold mb-2">Ages 9-18</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>Strength Evaluations</li>
              <li>Endurance Assessments</li>
              <li>Speed Measurements</li>
            </ul>
          </motion.div>
        </div>
      </motion.div>

      {/* Key Features Carousel */}
      <motion.div variants={itemVariants} className="mb-12">
        <h3 className="text-2xl font-bold mb-6 text-center">Key Features</h3>
        <div className="relative">
          <div className="overflow-hidden rounded-xl bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 p-6 shadow-lg border border-gray-200 dark:border-gray-700">
            <motion.div
              key={activeFeature}
              initial="hidden"
              animate="visible"
              variants={featureVariants}
              className="flex items-start space-x-4"
            >
              <div className="text-4xl bg-white dark:bg-gray-800 h-14 w-14 flex items-center justify-center rounded-full shadow-md">
                {features[activeFeature].icon}
              </div>
              <div>
                <h4 className="text-xl font-bold mb-2">{features[activeFeature].title}</h4>
                <p className="text-gray-700 dark:text-gray-300">{features[activeFeature].description}</p>
              </div>
            </motion.div>
          </div>
          
          {/* Indicators */}
          <div className="flex justify-center mt-4 space-x-2">
            {features.map((_, index) => (
              <button
                key={index}
                onClick={() => setActiveFeature(index)}
                className={`h-2 rounded-full transition-all ${
                  activeFeature === index ? "w-8 bg-blue-600" : "w-2 bg-gray-300 dark:bg-gray-600"
                }`}
                aria-label={`Feature ${index + 1}`}
              />
            ))}
          </div>
        </div>
      </motion.div>

      {/* Full Features List (Expandable) */}
      <motion.div 
        variants={itemVariants}
        className="mb-12"
      >
        <details className="group">
          <summary className="text-lg font-semibold cursor-pointer flex items-center">
            <span className="mr-2">View All Features</span>
            <svg className="w-5 h-5 group-open:rotate-180 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </summary>
          <div className="mt-4 pl-4 border-l-2 border-blue-500 space-y-4">
            {features.map((feature, index) => (
              <div key={index} className="pt-2">
                <h4 className="font-bold flex items-center">
                  <span className="text-green-500 mr-2">✅</span>
                  {feature.title}
                </h4>
                <p className="text-gray-700 dark:text-gray-300 pl-7">{feature.description}</p>
              </div>
            ))}
          </div>
        </details>
      </motion.div>

      {/* CTA */}
      <motion.div 
        className="text-center"
        variants={itemVariants}
      >
        <Link 
          to="/user-input" 
          className="inline-block bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-3 px-8 rounded-lg shadow-lg transition-all duration-300 hover:scale-105 hover:shadow-xl"
        >
          Get Started Now
        </Link>
        <p className="mt-4 text-gray-600 dark:text-gray-400">
          Start assessing your athletes and discover their perfect sports match today!
        </p>
      </motion.div>
    </motion.div>
  );
};

export default Home;