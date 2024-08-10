import React, { useState } from "react";
import {
  Button,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  Input,
  useDisclosure,
} from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import users from "../../data/users"; // Import users data
import { useToast } from "@chakra-ui/react";

const Login: React.FC = () => {
  const toast = useToast();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const { login } = useAuth();
  const { isOpen, onOpen, onClose } = useDisclosure();

  const handleLogin = () => {
    // Authentication logic using the imported users data
    const user = users.find(
      (user) => user.username === username && user.password === password
    );
    if (user) {
      localStorage.setItem("auth", "true");
      localStorage.setItem("fullname", user.fullName);
      toast({
        title: "Login successful.",
        description: "Welcome back!",
        status: "success",
        duration: 1500,
        isClosable: true,
        position: "top-right",
      });
      login();
      navigate("/");
      onClose();
    } else {
      toast({
        title: "Login failed.",
        description: "Invalid credentials. Please try again.",
        status: "error",
        duration: 1500,
        isClosable: true,
        position: "top-right",
      });
    }
  };

  return (
    <>
      <Button onClick={onOpen}>Login</Button>

      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Login</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Input
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              mb={4}
            />
            <Input
              placeholder="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </ModalBody>

          <ModalFooter>
            <Button colorScheme="blue" mr={3} onClick={handleLogin}>
              Login
            </Button>
            <Button variant="ghost" onClick={onClose}>
              Cancel
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
};

export default Login;
