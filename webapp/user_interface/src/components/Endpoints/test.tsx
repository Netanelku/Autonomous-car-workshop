import React, { useEffect, useState } from 'react';
import './spinner.css';
import './spinner1.css';
import Modal from './modal';

const Test: React.FC = () => {
  const [carAddress, setCarAddress] = useState("");
  const [loading, setLoading] = useState(true);
  const [connection, setConnection] = useState(false);

  useEffect(() => {
    if (carAddress !== "") {
      fetch("http://localhost:8080/health")
        .then(response => {
          // Handle response
          console.log(response);
        })
        .catch(error => {
          // Handle error
          console.error(error);
        });
    }
  }, [carAddress]);

  if (!carAddress)
    return <Modal />;

  return (
    <div className='spinner_wrapper'>
      <span className="loader"></span>
      <span className="loader1"></span>
    </div>
  );
}

export default Test;
