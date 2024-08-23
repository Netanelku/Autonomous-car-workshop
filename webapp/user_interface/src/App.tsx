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

  const fetchIpAddress = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8080/car/currentAddress");
      if (response.ok) {
        const data = await response.json();
        return data; // Return the data from the response
      } else {
        console.error("Failed to fetch IP address:", response.statusText);
        return null;
      }
    } catch (error) {
      console.error("Error fetching IP address:", error);
      return null;
    }
  };

  // useEffect to fetch IP address on component mount
  useEffect(() => {
    console.log("App is mounted.");
    const getIpAddress = async () => {
      const data = await fetchIpAddress(); // Wait for the data to be fetched
      if (data && data.current_ip) {
        setCurrentIpAddress(data.current_ip); // Update the state with the fetched IP
      }
    };
    getIpAddress();
  }, []); // Empty dependency array ensures this runs only once on mount

  // useEffect to handle connection logic based on the current IP address
  useEffect(() => {
    const handleConnectionCheck = async () => {
      setIsConnected(false);

      if (currentIpAddress !== "") {
        checkAttemptsRef.current = 0;
        const response = await fetchIpAddress(); // Fetch the IP address again
        console.log("aa");
        if (response && response.current_ip !== currentIpAddress) {
          console.log("bb");
          await updateIpAddress(currentIpAddress);
        }

        startConnectionCheck();
      }
    };

    handleConnectionCheck();

    return () => {
      stopConnectionCheck();
    };
  }, [currentIpAddress]); // Dependency array with currentIpAddress
  const updateIpAddress = async (newIp: any) => {
    try {
      const response = await fetch("http://127.0.0.1:8080/car/updateAddress", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ new_ip: newIp }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log("IP address updated successfully:", data.new_ip);
      } else {
        console.error("Failed to update IP address:", response.statusText);
      }
    } catch (error) {
      console.error("Error updating IP address:", error);
    }
  };

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

  const checkConnection = async () => {
    console.log("Checking connection...");
    let connected = false;

    try {
      const healthResponse = await fetch("http://127.0.0.1:8080/health");
      if (healthResponse.ok) {
        const healthData = await healthResponse.json();
        if (healthData.status === "ok") {
          connected = true;
          setIsConnecting(false);
        }
      }
    } catch (error) {
      console.error("Error checking connection:", error);
    }

    setIsConnecting(true);
    setIsConnected(connected);
    console.log("IsConnected:", connected, "IsConnecting:", false);

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
