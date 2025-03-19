// src/components/results/SportRecommendation.jsx
import React from 'react';
import { motion } from 'framer-motion';

const SportRecommendation = ({ recommendations }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className="card"
    >
      <h2 className="text-2xl font-semibold mb-4">Recommended Sports</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {recommendations.map((sport, index) => (
          <div key={sport.name} className="border rounded-lg overflow-hidden">
            <div className="bg-primary-light dark:bg-primary-dark p-3 text-white">
              <div className="text-xs font-medium">Recommendation #{index + 1}</div>
              <div className="text-xl font-bold">{sport.name}</div>
            </div>
            
            <div className="p-4">
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                {sport.description}
              </p>
              
              <div className="mt-2">
                <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">Compatibility Score</div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                  <div 
                    className="bg-green-500 h-2.5 rounded-full" 
                    style={{ width: `${Math.round(sport.compatibilityScore * 100)}%` }}
                  ></div>
                </div>
                <div className="text-right text-xs mt-1">
                  {Math.round(sport.compatibilityScore * 100)}%
                </div>
              </div>
              
              <div className="mt-3">
                <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">Key Benefits</div>
                <div className="flex flex-wrap gap-1">
                  {sport.benefits.map((benefit, i) => (
                    <span key={i} className="text-xs px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded-full">
                      {benefit}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
};

export default SportRecommendation;