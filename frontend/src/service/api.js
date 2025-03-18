const API_BASE_URL = import.meta.env.VITE_APP_API_BASE_URL;

/**
 * Sends user input data (age, weight, height, gender) to the backend.
 * @param {Object} userData - The user data object.
 * @returns {Promise<Object>} - The response from the backend.
 */
export const sendUserInput = async (userData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/user_input`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to send user data");
    }

    return await response.json();
  } catch (error) {
    console.error("Error sending user input:", error);
    throw error;
  }
};
