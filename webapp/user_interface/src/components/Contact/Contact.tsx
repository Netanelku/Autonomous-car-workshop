import React, { useState } from "react";
import {
  Box,
  Heading,
  Input,
  Textarea,
  Button,
  VStack,
  useToast,
  Flex,
} from "@chakra-ui/react";
import backgroundImage from "../../images/background1.jpg"; // Adjust the path as needed

const Contact: React.FC = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const toast = useToast();

  const handleSubmit = () => {
    // Handle form submission (e.g., send an email or save to a database)
    toast({
      title: "Message Sent",
      description: "Thank you for reaching out. We will get back to you soon.",
      status: "success",
      duration: 3000,
      isClosable: true,
      position: "top-right",
    });
    setName("");
    setEmail("");
    setMessage("");
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
      justifyContent={"center"}
      alignItems={"center"}
    >
      <VStack
        spacing={10}
        p={5}
        borderRadius="50px"
        borderWidth={5}
        borderColor="blue"
        sx={{
          boxShadow: "-5px 1px 42px 29px rgba(12, 143, 148, 1)",
          WebkitBoxShadow: "-5px 1px 42px 29px rgba(12, 143, 148, 1)",
          MozBoxShadow: "-5px 1px 42px 29px rgba(12, 143, 148, 1)",
        }}
      >
        <Heading as="h1" size="xl">
          Contact Us
        </Heading>
        <Box w="full">
          <Input
            placeholder="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            mb={10}
            color={"white"}
          />
          <Input
            placeholder="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            mb={10}
          />
          <Textarea
            placeholder="Message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            mb={10}
            h={"40vh"}
          />
          <Flex mb={4} mr={4} justifyContent={"flex-end"}>
            {" "}
            <Button onClick={handleSubmit} colorScheme="teal">
              Send Message
            </Button>
          </Flex>
        </Box>
      </VStack>
    </Flex>
  );
};

export default Contact;
