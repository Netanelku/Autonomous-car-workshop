import React from 'react';
import './Homepage.css'
import box from '../../images/box.png'
import phone from '../../images/phone.png'
import location from '../../images/loc.png'
const Homepage: React.FC = () => {
    

  return (
    <div className='mainWindow'> 
        <div className="SecondRow">
          <div className='paragraph'>
            <span>Smart Retrieval</span>
            <p>step into the future</p>
            <button>Get Started</button>
          </div>
          <div className='images'></div>
        </div>
        <div className="ThirdRow">
     <div className="rectangle">
        <div className='rec1'><img src={box} alt="box"></img></div>
        
        <div className='rec2'>
          <span>Visual</span>
          <span>Recognition</span>
         </div>
      </div>
      <div className="rectangle">
      <div className='rec1'><img src={location} className='logo' alt="loc"></img> </div>
        
        <div className='rec2'>
        <span>Navigation</span>
      </div>
      </div>
      <div className="rectangle">
      <div className='rec1'><img src={phone} className='logo' alt="phone"></img></div>
        
        <div className='rec2'>
      <span>Remote</span>
          <span>Control</span></div> 
    </div>
    </div>
    </div>
  );
}

export default Homepage;
