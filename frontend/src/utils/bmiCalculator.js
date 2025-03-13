// src/utils/bmiCalculator.js
export const calculateBMI = (weight, height) => {
  // Convert height from cm to m
  const heightInMeters = height / 100;

  // Calculate BMI
  const bmi = weight / (heightInMeters * heightInMeters);

  // Return rounded to 1 decimal place
  return Math.round(bmi * 10) / 10;
};

export const getBMICategory = (bmi, age, gender) => {
  // 📌Different categories based on age and gender could be implemented here
  // This is a simplified version
  if (bmi < 18.5) {
    return "Underweight";
  } else if (bmi < 25) {
    return "Normal weight";
  } else if (bmi < 30) {
    return "Overweight";
  } else {
    return "Obese";
  }
};
