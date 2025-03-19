// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import { AssessmentProvider } from './context/AssessmentContext';
import Layout from './components/common/Layout';
import Home from './pages/Home';
import UserInput from './pages/UserInput';
import VideoUpload from './pages/VideoUpload';
import Analysis from './pages/Analysis';
import Results from './pages/Results';
import './styles/global.css';

// Main App component
function App() {
  return (
    // Provide theme and assessment context
    <ThemeProvider>
      <AssessmentProvider>
        {/* Set up routing */}
        <Router>
          {/* Apply common layout */}
          <Layout>
            {/* Define routes */}
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/user-input" element={<UserInput />} />
              <Route path="/video-upload" element={<VideoUpload />} />
              <Route path="/analysis" element={<Analysis />} />
              <Route path="/results" element={<Results />} />
            </Routes>
          </Layout>
        </Router>
      </AssessmentProvider>
    </ThemeProvider>
  );
}

export default App;