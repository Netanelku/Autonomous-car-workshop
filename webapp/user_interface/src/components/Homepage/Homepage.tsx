import React, { useState, useEffect } from "react";
import {
  Box,
  Flex,
  Image,
  Text,
  Button,
  VStack,
  Heading,
} from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

// Import images after other imports
import backgroundImage from "../../images/background1.jpg"; // Adjust the path as needed
const images = [
  require("../../images/1.jpeg"),
  require("../../images/2.jpeg"),
  require("../../images/3.jpeg"),
  require("../../images/4.jpeg"),
];

const Homepage: React.FC = () => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const intervalId = setInterval(() => {
      setCurrentImageIndex((prevIndex) => (prevIndex + 1) % images.length);
    }, 4000);

    return () => clearInterval(intervalId);
  }, []);

  const handleDotClick = (index: number) => {
    setCurrentImageIndex(index);
  };

  return (
    <Flex
      flex={1}
      bgImage={`url(${backgroundImage})`}
      bgSize="cover"
      bgPosition="center"
      bgRepeat="no-repeat"
      direction="row"
      color="white"
    >
      <Flex
        flex={2}
        flexDirection="column"
        align="flex-start"
        p={10}
        bgColor="rgba(0, 0, 0, 0.2)"
        borderRadius="md"
        boxShadow="lg"
      >
        <Flex flex={2} justifyContent={"center"} alignItems={"center"}>
          <Heading size="4xl" ml={10} mb={4} textShadow="0 0 10px #3252a8">
            Smart Retrieval Autonomous Car
          </Heading>
        </Flex>
        <Flex flex={5} flexDirection={"column"} ml={10}>
          <VStack alignItems="start" spacing={4} mb={8}>
            <Text fontSize="2xl" lineHeight="tall">
              Step into the future with our Smart Retrieval Autonomous Car.
            </Text>
            <Text fontSize="2xl" lineHeight="tall">
              This groundbreaking vehicle is designed to swiftly retrieve items
            </Text>
            <Text fontSize="2xl" lineHeight="tall">
              using wireless WiFi remote control and advanced mobile camera
              visual identification.
            </Text>
            <Text fontSize="2xl" lineHeight="tall">
              Experience unparalleled convenience and innovation with technology
            </Text>
            <Text fontSize="2xl" lineHeight="tall">
              that brings efficiency and ease to your daily life.
            </Text>
          </VStack>
          {isAuthenticated && (
            <Button
              w={"20%"}
              as="a"
              href="#"
              colorScheme="teal"
              size="lg"
              borderRadius="full"
              px={8}
              py={6}
              _hover={{ bg: "teal.600" }}
              onClick={() => {
                navigate("/launch");
              }}
            >
              Get Started
            </Button>
          )}
        </Flex>
      </Flex>
      <Flex flex={1} justify="center" align="center" direction="column" p={10}>
        <Image
          borderRadius="lg"
          boxShadow="xl"
          src={images[currentImageIndex]}
          boxSize="40vh"
          mb={4}
          objectFit="cover"
          transition="transform 0.5s ease-in-out"
          _hover={{ transform: "scale(1.05)" }}
        />
        <Flex justify="center" mt={4}>
          {images.map((_, index) => (
            <Box
              key={index}
              w={3}
              h={3}
              mx={1}
              bg={currentImageIndex === index ? "teal.400" : "gray.600"}
              borderRadius="full"
              cursor="pointer"
              onClick={() => handleDotClick(index)}
              _hover={{ bg: "teal.300" }}
              transition="background-color 0.3s"
            />
          ))}
        </Flex>
      </Flex>
    </Flex>
  );
};

export default Homepage;
