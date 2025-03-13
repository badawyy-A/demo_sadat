// src/components/common/Footer.jsx
import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-card-light dark:bg-card-dark shadow-inner py-6">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <p className="text-gray-600 dark:text-gray-400">
            © {new Date().getFullYear()} Fitness Assessment App
          </p>
          <div className="mt-4 md:mt-0">
            <p className="text-gray-600 dark:text-gray-400">
              Helping coaches identify athletic potential
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;