import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const USER_INPUT_URL = API_BASE_URL + import.meta.env.VITE_USER_INPUT_ENDPOINT;
const VIDEO_UPLOAD_URL =
  API_BASE_URL + import.meta.env.VITE_VIDEO_UPLOAD_ENDPOINT;

/**
 * Sends user input data (age, weight, height, gender) to the backend.
 * @param {Object} userData - The user data object.
 * @returns {Promise<Object>} - The response from the backend.
 */
export const sendUserInput = async (userData) => {
  try {
    const response = await fetch(USER_INPUT_URL, {
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

// Function to upload videos based on age range
export const uploadVideos = async (ageRange, videos) => {
  const formData = new FormData();

  // Append required videos based on age range
  if (ageRange === "5-8") {
    formData.append("plate_video", videos.coordination);
    formData.append("balance_video", videos.balance);
  } else if (ageRange === "9-18") {
    formData.append("pushup_video", videos.push_up);
    formData.append("curlup_video", videos.curl_up);
    formData.append("cardiovascular_video", videos.cardiovascular);
    formData.append("speed_video", videos.speed);
  }

  try {
    const response = await axios.post(
      `${VIDEO_UPLOAD_URL}/${ageRange}`,
      formData,
      {
        headers: { "Content-Type": "multipart/form-data" },
      }
    );

    return response.data;
  } catch (error) {
    console.error(
      "Error uploading videos:",
      error.response?.error || error.message
    );
    throw error;
  }
};
