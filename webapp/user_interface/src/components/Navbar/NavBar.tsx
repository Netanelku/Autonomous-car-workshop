import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Flex,
  Box,
  Image,
  Link as ChakraLink,
  Button,
  VStack,
  HStack,
  useToast,
  Stack,
  Avatar,
  Text,
  Tooltip,
  useColorModeValue,
  Divider,
  Icon,
  Spinner,
  useDisclosure,
} from "@chakra-ui/react";

import { Link as ReactRouterLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Login from "../Login/Login";
import logo from "../../images/logo.png";
import IpAddressModal from "./IpAddressModal";
import { AiOutlineReload } from "react-icons/ai";
import { useConnection } from "../context/ConnectionContext";

const NavBar: React.FC = () => {
  const [name, setName] = useState<string>("");
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const toast = useToast();
  const bg = useColorModeValue("#0c3567", "#1a202c");
  const color = useColorModeValue("white", "white");
  const {
    currentIpAddress,
    isConnected,
    isConnecting,
    handleReconnect,
    setCurrentIpAddress,
  } = useConnection();

  const { isOpen, onOpen, onClose } = useDisclosure();

  const handleLogout = () => {
    logout();
    navigate("/");
    toast({
      title: "Logout successful.",
      description: "You have been logged out.",
      status: "info",
      duration: 1500,
      isClosable: true,
      position: "top-right",
    });
  };

  useEffect(() => {
    const name = localStorage.getItem("fullname");
    if (name != null) {
      setName(name);
    }
  }, [isAuthenticated]);

  return (
    <Flex
      bg={"#022e51"}
      as="nav"
      justify="space-between"
      color={color}
      w="100%"
      alignContent={"center"}
      pl={5}
      pr={5}
      h={"100%"}
      opacity={"100%"}
    >
      <IpAddressModal
        onClose={onClose}
        isOpen={isOpen}
        currentIpAddress={currentIpAddress}
        setCurrentIpAddress={setCurrentIpAddress} // Pass the setCurrentIpAddress function here
      />
      <ChakraLink
        as={ReactRouterLink}
        to="/"
        aria-label="Home"
        alignContent={"center"}
        h={"100%"}
      >
        <Image src={logo} alt="Logo" boxSize="50px" />
      </ChakraLink>

      <HStack pl={50} spacing={10} flex={1}>
        <NavItem to="/" label="Home" />
        <Divider orientation="vertical" h={"75%"} />
        <NavItem to="/about" label="About" />
        {isAuthenticated && (
          <>
            <Divider orientation="vertical" h={"75%"} />
            <NavItem to="/launch" label="Launch" />
          </>
        )}
        <Divider orientation="vertical" h={"75%"} />
        <NavItem to="/contact" label="Contact" />
      </HStack>

      <Flex alignItems="center">
        {!isAuthenticated ? (
          <Login />
        ) : (
          <Stack direction="row" spacing={5} align="center">
            <Flex alignItems="center">
              <Flex align="center" justify="center" mr={4}>
                {!isConnecting && isConnected && (
                  <Tooltip label="Change IP Address">
                    <Flex
                      onClick={onOpen}
                      align="center"
                      justify="center"
                      p={2}
                      borderRadius="md"
                      color="white"
                      cursor="pointer"
                    >
                      <Box
                        mt={1}
                        h={3}
                        w={3}
                        bg={"green"}
                        borderRadius="full"
                      />
                      <Text as={"b"} fontSize="2xl" color={"green"} ml={3}>
                        Online
                      </Text>
                    </Flex>
                  </Tooltip>
                )}
                {!isConnecting && !isConnected && (
                  <Tooltip label="Click to Connect">
                    <Flex
                      onClick={onOpen}
                      cursor="pointer"
                      align="center"
                      justify="center"
                      p={2}
                      borderRadius="md"
                      color="white"
                    >
                      <Box mt={1} h={3} w={3} bg={"red"} borderRadius="full" />
                      <Text as={"b"} fontSize="2xl" color={"red"} ml={3}>
                        Offline
                      </Text>
                    </Flex>
                  </Tooltip>
                )}
                {isConnecting && (
                  <Tooltip label={`connecting to ${currentIpAddress}`}>
                    <Flex
                      align="center"
                      justify="center"
                      p={2}
                      borderRadius="md"
                      color="white"
                    >
                      <Spinner color="yellow.500" />
                      <Text as={"b"} fontSize="2xl" color={"yellow"} ml={3}>
                        Connecting
                      </Text>
                    </Flex>
                  </Tooltip>
                )}
                {!isConnected && !isConnecting && (
                  <Tooltip label="Reconnect" hasArrow>
                    <Flex
                      ml={2}
                      alignContent={"center"}
                      justifyContent={"center"}
                      onClick={handleReconnect}
                      cursor={"pointer"}
                    >
                      <AiOutlineReload size={30} />
                    </Flex>
                  </Tooltip>
                )}
              </Flex>
            </Flex>
            <Tooltip label={name}>
              <Avatar name={name} />
            </Tooltip>
            <Button onClick={handleLogout} colorScheme="teal">
              Logout
            </Button>
          </Stack>
        )}
      </Flex>
    </Flex>
  );
};

const NavItem: React.FC<{ to: string; label: string }> = ({ to, label }) => (
  <ChakraLink as={ReactRouterLink} to={to} _hover={{ textDecoration: "none" }}>
    <Box
      w="full"
      h={10}
      display="flex"
      alignItems="center"
      justifyContent="center"
      borderRadius={10}
      fontSize={"xl"}
      textColor={"#a3b4c8"}
      fontFamily="sans-serif"
      color="white"
    >
      {label}
    </Box>
  </ChakraLink>
);

export default NavBar;
