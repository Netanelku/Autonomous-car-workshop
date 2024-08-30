import React, { Suspense } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import NavBar from "./components/Navbar/NavBar";
import Home from "./components/Homepage/Homepage";
import Login from "./components/Login/Login";
import ProtectedRoute from "./components/ProtectedRoute/ProtectedRoute";
import Launch from "./components/Launch/Launch";
import { Box, Flex } from "@chakra-ui/react";
import Contact from "./components/Contact/Contact";
import About from "./components/About/About";
import { ConnectionProvider } from "./components/context/ConnectionContext";

const App: React.FC = () => {
  return (
    <ConnectionProvider>
      <Flex direction="column" minHeight="100vh" bg={"black"}>
        <Router>
          <Box h={"6vh"}>
            <NavBar />
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
              </Routes>
            </Suspense>
          </Flex>
        </Router>
      </Flex>
    </ConnectionProvider>
  );
};

export default App;
