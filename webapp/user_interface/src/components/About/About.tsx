import React from "react";
import { Box, Heading, Text, VStack, Flex } from "@chakra-ui/react";
import backgroundImage from "../../images/background1.jpg"; // Adjust the path as needed

const About: React.FC = () => {
  return (
    <Flex
      flex={1}
      direction="row"
      bgImage={`url(${backgroundImage})`}
      bgSize="cover"
      bgPosition="center"
      bgRepeat="no-repeat"
      color="white"
      justifyContent="center"
      alignItems="center"
      position="relative"
      overflow="hidden"
    >
      {/* Overlay for better text readability */}
      <Box position="absolute" top={0} left={0} width="100%" height="100%" />

      <VStack
        spacing={6}
        p={8}
        zIndex={1}
        w={"80vw"}
        h={"50vh"}
        borderRadius="lg"
        boxShadow="lg"
        align="start"
      >
        <Heading as="h1" size="2xl" mb={4}>
          About Smart Retrieval Autonomous Car
        </Heading>
        <Text fontSize="lg" mb={4}>
          We propose the creation of a Smart Retrieval Autonomous Car designed
          for swift item retrieval within designated areas. This cutting-edge
          vehicle integrates features like wireless WiFi remote control and a
          mobile camera for visual identification.
        </Text>
        <Text fontSize="lg" mb={4}>
          The primary goal is to develop an adaptable autonomous car with the
          ability to autonomously identify and retrieve items guided by remote
          visual commands. This innovative solution aims to streamline the
          retrieval process, offering a reliable and efficient method for
          locating and recovering specific items.
        </Text>
        <Text fontSize="lg">
          The Smart Retrieval Autonomous Car, equipped with advanced
          technologies like WiFi connectivity and visual recognition features,
          emerges as a versatile tool capable of catering to a range of
          applications. Through the integration of robust components, the
          autonomous car demonstrates resilience during operations, rendering it
          suitable for varied environments. This initiative resonates with our
          goal of developing an intuitive and efficient robotic system,
          providing a valuable solution for tasks necessitating accurate item
          identification and retrieval within specified areas.
        </Text>
      </VStack>
    </Flex>
  );
};

export default About;
