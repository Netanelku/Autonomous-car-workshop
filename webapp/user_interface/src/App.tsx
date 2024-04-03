import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import NavBar from './components/Navbar/NavBar';
 import Home from './components/Homepage/Homepage';
// import About from './About';
// import Services from './Services';
// import Contact from './Contact';
const App: React.FC = ()=> {
  return (
    <div className="App">
      <div className='column1'></div>
      <div className='column2'>
      <Router>
      
      <NavBar />
          <Routes>
          <Route path="/" element={<Home/>} />
          {/* <Route path="/about" component={About} />
          <Route path="/services" component={Services} />
          <Route path="/contact" component={Contact} /> */}
          </Routes>

    </Router>
     </div>
     </div>
  );
}

export default App;
