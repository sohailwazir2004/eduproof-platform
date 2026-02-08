import React from 'react';
import { Link } from 'react-router-dom';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-white border-t border-gray-200 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="text-sm text-gray-600">
            &copy; {currentYear} EduProof. All rights reserved.
          </div>

          <div className="flex items-center gap-6">
            <Link
              to="/about"
              className="text-sm text-gray-600 hover:text-primary-600 transition-colors"
            >
              About
            </Link>
            <Link
              to="/privacy"
              className="text-sm text-gray-600 hover:text-primary-600 transition-colors"
            >
              Privacy Policy
            </Link>
            <Link
              to="/terms"
              className="text-sm text-gray-600 hover:text-primary-600 transition-colors"
            >
              Terms of Service
            </Link>
            <Link
              to="/support"
              className="text-sm text-gray-600 hover:text-primary-600 transition-colors"
            >
              Support
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
