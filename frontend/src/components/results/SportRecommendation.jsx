import React from 'react';

const SportRecommendation = ({ recommendations }) => {
  // Ensure we have an array of recommendations
  const processedRecommendations = React.useMemo(() => {
    // If it's already an array, return it
    if (Array.isArray(recommendations)) {
      return recommendations;
    }
    
    // If it's empty or undefined, return empty array
    if (!recommendations || (Array.isArray(recommendations) && recommendations.length === 0)) {
      return [];
    }
    
    // If it's an object with keys (name -> details)
    if (typeof recommendations === 'object' && recommendations !== null) {
      return Object.entries(recommendations).map(([name, details]) => ({
        name,
        description: typeof details === 'object' ? details.description || '' : '',
        compatibilityScore: typeof details === 'object' && details.score ? 
          parseFloat(details.score) / 100 : 0.8
      }));
    }
    
    // If it's a string (like in the sample API response), parse it
    if (typeof recommendations === 'string') {
      return recommendations
        .split('\n')
        .filter(item => item.trim())
        .map((item, index) => {
          // Remove numbers and periods from the beginning (e.g., "1. Tennis" -> "Tennis")
          const name = item.replace(/^\d+\.\s*/, '').trim();
          
          // Calculate compatibility score - higher for first recommendations
          const compatibilityScore = 0.95 - (index * 0.05);
          
          return {
            name,
            compatibilityScore,
            description: getSportDescription(name)
          };
        });
    }
    
    return [];
  }, [recommendations]);

  // Function to generate descriptions for sports
  const getSportDescription = (sportName) => {
    const descriptions = {
      'Tennis': 'Great for developing hand-eye coordination, agility, and cardiovascular fitness.',
      'Badminton': 'Excellent for developing reflexes, coordination, and aerobic endurance.',
      'Gymnastics': 'Perfect for building strength, flexibility, balance, and body control.',
      'Swimming': 'Develops overall body strength, cardiovascular fitness, and coordination.',
      'Soccer': 'Improves cardiovascular endurance, coordination, and teamwork skills.',
      'Basketball': 'Great for developing coordination, agility, and cardiovascular endurance.',
      'Volleyball': 'Builds upper body strength, hand-eye coordination, and teamwork.',
      'Dance': 'Excellent for developing flexibility, coordination, and artistic expression.',
      'Martial Arts': 'Develops discipline, coordination, and overall body strength.',
      'Athletics': 'Great for building speed, strength, and cardiovascular endurance.'
    };
    
    return descriptions[sportName] || 'This sport aligns well with your physical capabilities and fitness profile.';
  };

  return (
    <div className="card">
      <h2 className="text-2xl font-semibold mb-4">Recommended Sports</h2>
      
      {processedRecommendations.length === 0 ? (
        <p className="text-gray-600 dark:text-gray-400">No recommendations available.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {processedRecommendations.slice(0, 6).map((sport, index) => (
            <div 
              key={index} 
              className="border rounded-lg p-4 flex flex-col"
            >
              <div className="flex justify-between items-center mb-2">
                <h3 className="text-xl font-medium">{sport.name}</h3>
                <span className="bg-primary-DEFAULT text-white px-2 py-1 rounded text-sm">
                  {Math.round((sport.compatibilityScore || 0) * 100)}% Match
                </span>
              </div>
              
              <p className="text-gray-600 dark:text-gray-400 flex-grow">
                {sport.description || 'This sport aligns well with your physical capabilities and fitness profile.'}
              </p>
              
              <div className="mt-3 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div 
                  className="bg-primary-DEFAULT h-2 rounded-full" 
                  style={{ width: `${Math.round((sport.compatibilityScore || 0) * 100)}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      )}
      
      <div className="mt-6">
        <h3 className="text-lg font-medium mb-2">How were these sports selected?</h3>
        <p className="text-gray-600 dark:text-gray-400">
          These recommendations are based on your physical fitness assessment results. 
          Sports that align with your strengths in coordination, balance, and strength 
          are prioritized to maximize your performance potential and enjoyment.
        </p>
      </div>
    </div>
  );
};

export default SportRecommendation;