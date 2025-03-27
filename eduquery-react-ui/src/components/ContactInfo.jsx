import React from 'react';

const ContactInfo = () => {
  return (
    <div className="mt-5 d-flex flex-wrap gap-4 align-items-center">
      <div>
        <a href="mailto:rohitmapakshi@gmail.com" className="text-decoration-none">
          <strong>Email</strong>
        </a>
      </div>
      <div>
        <a
          href="https://www.linkedin.com/in/rohit-mapakshi/"
          target="_blank"
          rel="noopener noreferrer"
          className="text-decoration-none"
        >
          <strong>LinkedIn</strong>
        </a>
      </div>
      <div>
        <a
          href="https://github.com/rohit-mapakshi97"
          target="_blank"
          rel="noopener noreferrer"
          className="text-decoration-none"
        >
          <strong>GitHub</strong>
        </a>
      </div>
      <div>
        <a
          href="https://rohitmapakshi.com/"
          target="_blank"
          rel="noopener noreferrer"
          className="text-decoration-none"
        >
          <strong>Portfolio</strong>
        </a>
      </div>
    </div>
  );
};

export default ContactInfo;
