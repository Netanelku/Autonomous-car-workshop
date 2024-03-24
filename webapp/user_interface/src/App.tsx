import React from 'react';
import './App.css';

const App: React.FC = ()=> {
  return (
    <div className="App">
      <div className="FirstRow">
        <div className="menu"> 
        <div className="menu1"></div>
        <div className="menu1"></div>
        {/* <div className="menu1"></div>
        <div className="menu1"></div>
        <div className="menu1"></div>
        <div className="menu1"></div> */}
        </div>
      </div>
     
     <div className="SecondRow">bbb</div>
     <div className="ThirdRow">
      <div className="rectangle">
        <div className='rec1'>Image </div>
        
        <div className='rec2'>text </div>
      </div>
      <div className="rectangle"></div>
      <div className="rectangle"></div>
     </div>
    </div>
  );
}

export default App;
