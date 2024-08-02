// components/Homepage/Homepage.tsx
import React, { useState, useEffect } from "react";
// import { ChevronLeftIcon, ChevronRightIcon } from "@chakra-ui/icons";

import {
  Box,
  Flex,
  Image,
  Text,
  Button,
  Stack,
  Heading,
} from "@chakra-ui/react";
import car from "../../images/car.png";
import { useAuth } from "../context/AuthContext";
import backgroundImage from "../../images/background1.jpg"; // Adjust the path as needed
const images = [
  require("../../images/1.jpeg"),
  require("../../images/2.jpeg"),
  require("../../images/3.jpeg"),
  require("../../images/4.jpeg"),
];
const Homepage: React.FC = () => {
  const text =
    "Step into the future with our Smart Retrieval Autonomous Car. This groundbreaking vehicle is designed to swiftly retrieve items using wireless WiFi remote control and advanced mobile camera visual identification. Experience unparalleled convenience and innovation with technology that brings efficiency and ease to your daily life.";
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  const { isAuthenticated } = useAuth();
  const handleDotClick = (index: number) => {
    setCurrentImageIndex(index);
  };
  useEffect(() => {
    const intervalId = setInterval(() => {
      setCurrentImageIndex((prevIndex) => (prevIndex + 1) % images.length);
    }, 4000);

    // Cleanup interval on component unmount
    return () => clearInterval(intervalId);
  }, []);
  return (
    <Flex
      flex={1}
      bgImage={`url(${backgroundImage})`}
      bgSize="cover"
      bgPosition="center"
      bgRepeat="no-repeat"
      // bg="gray.900" // Fallback background color
      direction="row"
      color="white"
    >
      <Flex
        flexDirection="column"
        flex={2}
        // justifyContent="center"

        // mb={{ base: 10, md: 0 }}
      >
        <Heading
          as="h1"
          size={"4xl"}
          mb={6}
          lineHeight="short"
          position={"relative"}
          left={"10%"}
          top={"10%"}
        >
          Smart Retrieval Car
        </Heading>
        <Text
          fontSize={"3xl"}
          mt={20}
          w={"80%"}
          lineHeight="tall"
          position={"relative"}
          left={"10%"}
          top={"10%"}
          flexWrap={"nowrap"}
          mb={20}
        >
          {text}
        </Text>
        <Button
          w={"10%"}
          position={"relative"}
          left={"10%"}
          top={"10%"}
          as="a"
          href={isAuthenticated ? "launch" : "login"}
          colorScheme="teal"
          size="lg"
          borderRadius="full"
          px={8}
          py={6}
        >
          Get Started
        </Button>
      </Flex>
      <Flex
        flex="1"
        h={"100%"}
        position="relative"
        justify="center"
        align="center"
        direction={"column"}
      >
        <Image
          borderRadius={50}
          boxShadow={5}
          src={images[currentImageIndex]}
          boxSize={"50vh"}
          mb={10}
          // boxSize={{ base: "75vw", md: "40vw" }}
          objectFit="cover"
          transition="all 0.5s ease"
        />
        <Flex justify="center" mt={4} px={5}>
          {images.map((_, index) => (
            <Box
              px={5}
              key={index}
              w={3}
              h={3}
              mx={1}
              bg={currentImageIndex === index ? "teal.400" : "gray.600"}
              borderRadius="full"
              cursor="pointer"
              onClick={() => handleDotClick(index)}
            />
          ))}
        </Flex>
      </Flex>
    </Flex>
  );
};

export default Homepage;
