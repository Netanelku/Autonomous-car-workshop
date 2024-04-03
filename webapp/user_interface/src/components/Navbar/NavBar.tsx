import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import logo from "../../images/logo.png";

const NavBar: React.FC = () => {
  const [darkMode, setDarkMode] = useState<boolean>(false);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <nav className="d-flex h-20 mw-100">
      <div className="d-flex justify-content-left d-flex align-items-center mt-3 text-white ">
        <div className="d-flex pl-2 mx-4"> {/* Use flexbox to align items */}
          <Link to="/" className="navbar-brand"><img src={logo} className='logo' alt="Logo"></img></Link>
        </div>
        <ul className="d-flex flex-row list-unstyled "> {/* Use ml-auto to push routes to the right */}
          <li className="nav-item mx-5">
            <Link to="/" className="nav-link">Home</Link>
          </li>
          <li className="nav-item mx-5">
            <Link to="/about" className="nav-link ">About</Link>
          </li>
          <li className="nav-item mx-5">
            <Link to="/launch" className="nav-link">Launch</Link>
          </li>
          <li className="nav-item mx-5">
            <Link to="/contact" className="nav-link">Contact</Link>
          </li>
        </ul>
     
      </div>
    </nav>
  );
}

export default NavBar;
