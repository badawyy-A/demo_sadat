
// src/components/common/Navbar.jsx
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import ThemeToggle from './ThemeToggle';

const Navbar = () => {
  const location = useLocation();
  
  const navLinks = [
    { name: 'Home', path: '/' },
    { name: 'User Input', path: '/user-input' },
    { name: 'Video Upload', path: '/video-upload' },
    { name: 'Results', path: '/results' }
  ];

  return (
    <nav className="bg-card-light dark:bg-card-dark shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <Link to="/" className="text-xl font-bold text-primary-dark dark:text-primary-light">
            Fitness Assessment App
          </Link>
          
          <div className="flex items-center space-x-4">
            <div className="hidden md:flex space-x-4">
              {navLinks.map((link) => (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`px-3 py-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 ${
                    location.pathname === link.path
                      ? 'font-semibold text-primary-dark dark:text-primary-light'
                      : 'text-gray-700 dark:text-gray-300'
                  }`}
                >
                  {link.name}
                </Link>
              ))}
            </div>
            <ThemeToggle />
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;