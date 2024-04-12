import React from 'react';
import './Homepage.css'
import './button.css'
import box from '../../images/box.png'
import phone from '../../images/phone.png'
import location from '../../images/loc.png'
import car from "../../images/car.png"
const Homepage: React.FC = () => {
    let text="Step into the future with our Smart Retrieval Autonomous Car,\n a groundbreaking vehicle designed to swiftly retrieve items using\n wireless WiFi remote control and mobile camera visual identification."
    let lines = text.split("\n");
    let paragraphs = lines.map(line => `<p>${line}</p>`);
    let html = paragraphs.join("");
  return (
    <div className='mainWindow'> 
        <div className="SecondRow">
          <div className='paragraph'>
            <h1 >Smart Retrieval</h1>
            <div>{lines.map((line,index)=>(<p key={index}>{line}</p>))}</div>
            <a href="launch" className="animated-button12">Get Started</a>
          </div>
          <div className='images'>
            <img src={car} alt="car"></img></div>
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
