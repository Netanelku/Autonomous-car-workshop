import React, { Suspense, useState, useEffect, useRef } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import NavBar from "./components/Navbar/NavBar";
import Home from "./components/Homepage/Homepage";
import Login from "./components/Login/Login";
import ProtectedRoute from "./components/ProtectedRoute/ProtectedRoute";
import Launch from "./components/Launch/Launch";
import { Box, Flex, Button } from "@chakra-ui/react";
import { useAuth } from "./components/context/AuthContext";
import Contact from "./components/Contact/Contact";
import About from "./components/About/About";

const App: React.FC = () => {
  const { isAuthenticated, logout } = useAuth();

  const [currentIpAddress, setCurrentIpAddress] = useState<string>(() => {
    return localStorage.getItem("currentIpAddress") || "";
  });
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [isConnecting, setIsConnecting] = useState<boolean>(false);

  const checkAttemptsRef = useRef(0);
  const intervalIdRef = useRef<number | undefined>(undefined);

  useEffect(() => {
    localStorage.setItem("currentIpAddress", currentIpAddress);

    setIsConnected(false);
    checkAttemptsRef.current = 0;

    startConnectionCheck();

    return () => {
      stopConnectionCheck();
    };
  }, [currentIpAddress]);

  const startConnectionCheck = () => {
    stopConnectionCheck(); // Clear any existing interval

    intervalIdRef.current = window.setInterval(() => {
      checkConnection();
    }, 10000);
  };

  const stopConnectionCheck = () => {
    if (intervalIdRef.current !== undefined) {
      clearInterval(intervalIdRef.current);
    }
  };

  const checkConnection = () => {
    console.log("Checking connection...");

    const connected = Math.random() >= 0.5; // Simulate connection check
    setIsConnecting(true);
    setIsConnected(connected);
    setIsConnecting(!connected);
    console.log("IsConnected", connected, "isConnecting", !connected);

    if (!connected) {
      checkAttemptsRef.current += 1;
    } else {
      checkAttemptsRef.current = 0; // Reset counter if connected
    }

    if (checkAttemptsRef.current >= 4) {
      setIsConnecting(false);
      stopConnectionCheck();
      console.log("Stopped checking after 4 unsuccessful attempts.");
    }
  };

  const handleReconnect = () => {
    checkAttemptsRef.current = 0;
    setIsConnecting(true);
    startConnectionCheck();
  };

  return (
    <Flex direction="column" minHeight="100vh" bg={"black"}>
      <Router>
        <Box h={"6vh"}>
          <NavBar
            setCurrentIpAddress={setCurrentIpAddress}
            currentIpAddress={currentIpAddress}
            isConnected={isConnected}
            isConnecting={isConnecting}
            handleReconnect={handleReconnect}
          />
        </Box>
        <Flex flex={1} direction="column">
          <Suspense fallback={<Box>Loading...</Box>}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/contact" element={<Contact />} />
              <Route path="/about" element={<About />} />
              <Route
                path="/launch"
                element={<ProtectedRoute element={<Launch />} />}
              />
              {/* Add more protected routes as needed */}
            </Routes>
          </Suspense>
        </Flex>
      </Router>
    </Flex>
  );
};

export default App;
