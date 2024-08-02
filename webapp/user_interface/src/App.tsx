// App.tsx
import React, { Suspense } from "react";
// import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import NavBar from "./components/Navbar/NavBar";
import Home from "./components/Homepage/Homepage";
import Login from "./components/Login/Login";
import { AuthProvider } from "./components/context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute/ProtectedRoute";
import Launch from "./components/Launch/Launch";
import { Box, Flex } from "@chakra-ui/react";

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Flex direction="column" minHeight="100vh" bg={"black"}>
        <Router>
          <Box h={"6vh"}>
            <NavBar />
          </Box>
          <Flex flex={1}>
            <Suspense fallback={<Box>Loading...</Box>}>
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
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
    </AuthProvider>
  );
};

export default App;
