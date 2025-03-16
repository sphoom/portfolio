// index.jsx
import React from "react"; 
import { Education } from "./Education";
import { Experience } from "./Experience";
import { FeaturedProjects } from "./FeaturedProjects";
import { Navbar } from "./Navbar";
import line1 from "./line-1.svg";
import line2 from "./line-2.svg";
import line3 from "./line-3.svg";
import line4 from "./line-4.svg";
import "./style.css";
import upworkIcon from "./upwork-icon.svg";

export const PortfolioDark = () => {
  return (
    <div className="portfolio-dark">
      <Navbar />
      <div className="container">
        <h1 className="title">Your Name</h1>
        <h2 className="subtitle">Hey, I’m</h2>
        <p className="description">
          I'm a data scientist and product analyst passionate about finance and marketing analytics.
          My projects focus on A/B testing, predictive modeling, and data-driven decision-making.
        </p>
        <div className="contact-buttons">
          <a href="mailto:your-email@example.com" className="btn">Email</a>
          <a href="https://github.com/yourprofile" className="btn">GitHub</a>
          <a href="https://linkedin.com/in/yourprofile" className="btn">LinkedIn</a>
        </div>
        <FeaturedProjects />
        <Education />
        <Experience />
      </div>
      <footer className="footer">&copy; 2025 Your Name. All Rights Reserved.</footer>
    </div>
  );
};
