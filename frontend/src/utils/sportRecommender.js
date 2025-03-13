// src/utils/sportRecommender.js
// This is a simplified sports database with fitness attributes
const sportsDatabase = [
  {
    name: "Soccer",
    attributes: {
      cardiovascular: 0.9,
      speed: 0.8,
      coordination: 0.7,
      flexibility: 0.5,
      balance: 0.6,
      muscularStrength: 0.6,
    },
    description:
      "A team sport involving running, kicking, and strategic positioning.",
    suitableAges: "5-18",
    benefits: ["Teamwork", "Cardiovascular health", "Coordination"],
  },
  {
    name: "Swimming",
    attributes: {
      cardiovascular: 0.9,
      muscularStrength: 0.7,
      flexibility: 0.8,
      coordination: 0.6,
      balance: 0.5,
      speed: 0.7,
    },
    description:
      "An individual or team water sport that builds overall fitness.",
    suitableAges: "5-18",
    benefits: [
      "Full-body workout",
      "No impact on joints",
      "Respiratory strength",
    ],
  },
  {
    name: "Gymnastics",
    attributes: {
      balance: 0.9,
      flexibility: 0.9,
      muscularStrength: 0.8,
      coordination: 0.9,
      speed: 0.6,
      cardiovascular: 0.6,
    },
    description:
      "A sport involving exercises requiring balance, strength, flexibility, agility, and coordination.",
    suitableAges: "5-16",
    benefits: ["Body awareness", "Strength", "Discipline"],
  },
  {
    name: "Basketball",
    attributes: {
      speed: 0.8,
      coordination: 0.8,
      cardiovascular: 0.8,
      muscularStrength: 0.7,
      balance: 0.7,
      flexibility: 0.5,
    },
    description:
      "A team sport requiring speed, coordination and strategic play.",
    suitableAges: "8-18",
    benefits: ["Teamwork", "Strategic thinking", "Hand-eye coordination"],
  },
  {
    name: "Tennis",
    attributes: {
      coordination: 0.9,
      speed: 0.8,
      cardiovascular: 0.7,
      flexibility: 0.7,
      balance: 0.8,
      muscularStrength: 0.6,
    },
    description: "A racket sport that can be played individually or in teams.",
    suitableAges: "6-18",
    benefits: ["Hand-eye coordination", "Agility", "Strategic thinking"],
  },
  {
    name: "Track and Field",
    attributes: {
      speed: 0.9,
      cardiovascular: 0.9,
      muscularStrength: 0.8,
      flexibility: 0.7,
      coordination: 0.6,
      balance: 0.6,
    },
    description:
      "A collection of sports events including running, jumping, and throwing.",
    suitableAges: "8-18",
    benefits: ["Individual performance", "Discipline", "Speed and power"],
  },
  {
    name: "Martial Arts",
    attributes: {
      balance: 0.9,
      coordination: 0.8,
      flexibility: 0.8,
      muscularStrength: 0.8,
      speed: 0.7,
      cardiovascular: 0.7,
    },
    description:
      "Combat practices involving training for self-defense and discipline.",
    suitableAges: "6-18",
    benefits: ["Self-discipline", "Focus", "Self-defense skills"],
  },
  {
    name: "Volleyball",
    attributes: {
      coordination: 0.8,
      muscularStrength: 0.7,
      speed: 0.7,
      cardiovascular: 0.7,
      flexibility: 0.6,
      balance: 0.7,
    },
    description: "A team sport where players hit a ball over a net.",
    suitableAges: "10-18",
    benefits: ["Teamwork", "Hand-eye coordination", "Reflexes"],
  },
  {
    name: "Dance",
    attributes: {
      flexibility: 0.9,
      coordination: 0.9,
      balance: 0.9,
      cardiovascular: 0.7,
      muscularStrength: 0.6,
      speed: 0.6,
    },
    description: "An artistic and athletic expression through movement.",
    suitableAges: "5-18",
    benefits: ["Artistic expression", "Rhythm", "Flexibility"],
  },
  {
    name: "Rowing",
    attributes: {
      muscularStrength: 0.9,
      cardiovascular: 0.9,
      coordination: 0.7,
      balance: 0.7,
      flexibility: 0.6,
      speed: 0.6,
    },
    description: "A water sport using oars to propel a boat.",
    suitableAges: "12-18",
    benefits: ["Full-body workout", "Teamwork", "Endurance"],
  },
];

// Function to normalize test scores to a 0-1 scale
const normalizeScores = (testResults) => {
  const normalized = {};
  for (const [test, score] of Object.entries(testResults)) {
    // Assuming scores are between 0-100
    normalized[test] = score / 100;
  }
  return normalized;
};

// Function to calculate compatibility score between candidate and sport
const calculateCompatibility = (normalizedScores, sport) => {
  let totalScore = 0;
  let attributeCount = 0;

  for (const [attribute, weight] of Object.entries(sport.attributes)) {
    if (normalizedScores[attribute]) {
      totalScore += normalizedScores[attribute] * weight;
      attributeCount++;
    }
  }

  // If we have scores for all attributes, divide by attributeCount
  // Otherwise, normalize based on available attributes
  return attributeCount > 0 ? totalScore / attributeCount : 0;
};

// Main function to recommend sports
export const recommendSports = (testResults, userData) => {
  const age = parseInt(userData.age);
  const normalizedScores = normalizeScores(testResults);

  // Calculate compatibility for each sport
  const sportScores = sportsDatabase.map((sport) => {
    const compatibilityScore = calculateCompatibility(normalizedScores, sport);
    return {
      ...sport,
      compatibilityScore,
    };
  });

  // Sort by compatibility score and return top 3
  return sportScores
    .sort((a, b) => b.compatibilityScore - a.compatibilityScore)
    .slice(0, 3);
};
