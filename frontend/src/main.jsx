// src/index.jsx
import React from "react";
import ReactDOM from "react-dom/client"; 
import App from "./App";  
// Create a root element to render the app into the DOM
const root = ReactDOM.createRoot(document.getElementById("root"));

// Render the app inside StrictMode for development checks
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);