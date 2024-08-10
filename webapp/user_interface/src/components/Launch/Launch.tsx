import { Flex } from "@chakra-ui/react";
import React, { useState } from "react";
import backgroundImage from "../../images/background.jpg"; // Adjust the path as needed

const Launch: React.FC = () => {
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
    ></Flex>
  );
};

export default Launch;
