import React, { useState, useEffect } from "react";
import {
  Flex,
  Text,
  Box,
  Stack,
  Card,
  CardHeader,
  Heading,
  CardBody,
  Button,
  Image,
  Divider,
  Input,
  Textarea,
  Switch,
  FormControl,
  FormLabel,
  Slider,
  Icon,
  Fade,
  SliderTrack,
  SliderFilledTrack,
  SliderThumb,
  VStack,
  HStack,
  Slide,
  Tooltip,
  useToast,
} from "@chakra-ui/react";
import { Progress } from "@chakra-ui/react";
import { useAuth } from "../context/AuthContext";
import backgroundImage from "../../images/background.jpg"; // Adjust the path as needed
import CustomSteps from "./CustomSteps";
import tasks from "./tasks.json"; // Importing the JSON file
import { useConnection } from "../context/ConnectionContext";
import { FaRocket } from "react-icons/fa";

const Launch: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [selectedTask, setSelectedTask] = useState<any>(null);
  const [customTaskName, setCustomTaskName] = useState("");
  const [customTaskInstructions, setCustomTaskInstructions] = useState("");
  const [liveAudioStatus, setLiveAudioStatus] = useState(true);
  const [liveNotifications, setLiveNotifications] = useState(true);
  const [retryAttempts, setRetryAttempts] = useState(20);
  const [ledStatus, setLedStatus] = useState(true);
  const [showSceneDescription, setShowSceneDescription] = useState(true);
  const [isStep3Visible, setIsStep3Visible] = useState(false);
  // const [status, setStatus] = useState<string>("Idle");
  const toast = useToast(); // Initialize useToast
  const { isAuthenticated, logout } = useAuth();
  const { isConnected, isConnecting } = useConnection();
  const [percentage, setPercentage] = useState(0);
  const [textIndex, setTextIndex] = useState(0);
  const [isLaunched, setIsLaunched] = useState(false); // State to track if launched
  const [currentTask, setCurrentTask] = useState("");
  const [status, setStatus] = useState("");
  const [isTaskEnded, setIsTaskEnded] = useState(false);
  const [isSucceeded, setIsSucceeded] = useState(true);
  const promotionalTexts = [
    "Revolutionize retrieval with smart automation",
    "Boost efficiency with our autonomous car",
    "Get fast, reliable item retrieval now",
    "Experience seamless automation today",
    "Transform retrieval with cutting-edge tech",
    "Effortless item retrieval at your fingertips",
    "Innovative tech for faster retrieval",
    "Smart and efficient autonomous retrieval",
    "Upgrade to our advanced retrieval system",
    "Lead with the latest in smart technology",
  ];
  let percentageInterval: NodeJS.Timeout | null = null;
  let textInterval: NodeJS.Timeout | null = null;
  useEffect(() => {
    if (isLaunched && currentTask) {
      const fetchStatus = async () => {
        try {
          const response = await fetch(
            `http://127.0.0.1:8080/task/status/${currentTask}`
          );
          const data = await response.json();
          setPercentage(data.percentage_complete || 0);
          setStatus(data.event || "unknown");
          if (data.status === "success") {
            setIsSucceeded(true);
          } else {
            setIsSucceeded(false);
          }
        } catch (error) {
          console.error("Error fetching task status:", error);
        }
      };

      fetchStatus();
      percentageInterval = setInterval(fetchStatus, 2000);

      textInterval = setInterval(() => {
        setTextIndex((prev) => (prev + 1) % promotionalTexts.length);
      }, 3000);

      return () => {
        if (percentageInterval) {
          clearInterval(percentageInterval);
        }
        if (textInterval) {
          clearInterval(textInterval);
        }
      };
    }
  }, [isLaunched, currentTask, promotionalTexts.length]);

  useEffect(() => {
    if (currentStep === 3) {
      setIsStep3Visible(true);
    } else {
      setIsStep3Visible(false);
    }
  }, [currentStep]);

  const resetLaunchState = () => {
    // Reset all the relevant states
    setCurrentStep(1);
    setSelectedTask(null);
    setCustomTaskName("");
    setCustomTaskInstructions("");
    setLiveAudioStatus(true);
    setLiveNotifications(true);
    setRetryAttempts(20);
    setLedStatus(true);
    setShowSceneDescription(true);
    setIsStep3Visible(false);
    setPercentage(0);
    setTextIndex(0);
    setIsLaunched(false);
    setCurrentTask("");
    setStatus("");
    setIsTaskEnded(false);
    setIsSucceeded(true);

    // Clear all intervals or timeouts
    if (percentageInterval) {
      clearInterval(percentageInterval);
      percentageInterval = null;
    }
    if (textInterval) {
      clearInterval(textInterval);
      textInterval = null;
    }
  };

  const handleLaunchClick = async () => {
    try {
      const response = await fetch(
        `http://127.0.0.1:8080/car/create_task?target_object_id=${selectedTask.id}`
      );
      const data = await response.json();
      console.log(data.task_id);
      setCurrentTask(data.task_id);
      setIsLaunched(true);
      const response1 = await fetch(
        `http://127.0.0.1:8080/car/start_task?task_id=${data.task_id}`
      );

      if (!response1.ok) {
        throw new Error(`HTTP error! Status: ${response1.status}`);
      }
    } catch (error) {
      console.error("Error during fetch:", error);
    }
  };

  const handleTaskSelection = (taskId: number) => {
    const task = tasks.find((task) => task.id === taskId);
    setSelectedTask(task);
    setCustomTaskName(task?.title || "");
    setCustomTaskInstructions(task?.description || "");
  };

  const handleCustomizeTask = () => {
    console.log("Customized Task Name:", customTaskName);
    console.log("Customized Task Instructions:", customTaskInstructions);
    console.log("Live Audio Status:", liveAudioStatus);
    console.log("Live Notifications:", liveNotifications);
    console.log("Retry Attempts:", retryAttempts);
    console.log("LED Status:", ledStatus);
    setCurrentStep(3);
  };

  const updateRetryAttemptsOnServer = async (attempts: number) => {
    try {
      const response = await fetch(
        "http://127.0.0.1:8080/car/updateRetryAttempts",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ retryAttempts: attempts }),
        }
      );

      if (!response.ok) {
        console.error("Failed to update retry attempts:", response.statusText);
      } else {
        console.log("Retry attempts updated successfully on the server.");
      }
    } catch (error) {
      console.error("Error updating retry attempts:", error);
    }
  };

  useEffect(() => {
    updateRetryAttemptsOnServer(retryAttempts);
  }, [retryAttempts]);

  useEffect(() => {
    if (status != "") {
      if (liveAudioStatus && window.speechSynthesis) {
        const utterance = new SpeechSynthesisUtterance(`${status}.`);
        window.speechSynthesis.speak(utterance);
      }
      if (liveNotifications) {
        toast({
          position: "top-right",
          title: "Status Update",
          description: `${status}.`,
          status: "info",
          duration: 5000,
          isClosable: false,
        });
      }
    }
  }, [status, liveAudioStatus, liveNotifications, toast]);

  useEffect(() => {
    if (percentage == 100) {
      setIsTaskEnded(true);
    }
  }, [percentage]);
  return (
    <Flex
      flex={1}
      bgImage={`url(${backgroundImage})`}
      bgSize="cover"
      bgPosition="center"
      bgRepeat="no-repeat"
      direction="column"
      color="white"
    >
      <Flex flex={1} justifyContent={"center"}>
        {currentStep === 1 && (
          <Flex flexDirection={"row"} w={"50vw"} m={10}>
            <Flex
              flex={3}
              borderRadius="20px"
              borderWidth={5}
              borderColor="#001130"
              bgColor={"#031636"}
              flexDirection={"column"}
              sx={{
                boxShadow: "-2px 1px 20px 10px rgba(12, 143, 148, 1)",
              }}
            >
              <Box justifyContent={"center"} m={4} p={4} w={"100%"}>
                <Text fontSize={"2xl"} color={"white"} alignContent={"center"}>
                  Please Select a Task...
                </Text>
              </Box>
              <Flex flex={1} bg={"#011A3C"} p={4} borderRadius="20px">
                <Stack spacing="4" w={"100%"}>
                  {tasks.map((task) => (
                    <Card
                      key={task.id}
                      size={"md"}
                      w={"100%"}
                      bg={"#021D44"}
                      color="white"
                      borderColor="gray.600"
                      borderWidth={1}
                      _hover={{ bg: "#032656", cursor: "pointer" }}
                      onClick={() => handleTaskSelection(task.id)}
                    >
                      <CardHeader>
                        <Heading size="md">{task.title}</Heading>
                      </CardHeader>
                      <CardBody>
                        <Text>{task.description}</Text>
                      </CardBody>
                    </Card>
                  ))}
                </Stack>
              </Flex>
            </Flex>
            <Flex flex={1}></Flex>
            <Flex
              borderRadius="20px"
              borderWidth={5}
              borderColor="#001130"
              bgColor={"#00224D"}
              opacity={selectedTask ? 1 : 0.1}
              sx={{
                boxShadow: "-2px 1px 20px 10px rgba(12, 143, 148, 1)",
              }}
              flex={5}
              justifyContent={selectedTask ? "inherit" : "center"}
              alignItems={selectedTask ? "inherit" : "center"}
              flexDirection={"column"}
            >
              {selectedTask && (
                <>
                  <Flex
                    flex={1}
                    alignItems={"center"}
                    justifyContent={"center"}
                  >
                    <Image
                      w={"75%"}
                      h={"90%"}
                      bg={"white"}
                      src={selectedTask.image_path}
                      alt={selectedTask.title}
                      borderRadius="10px"
                      mb={4}
                    />
                  </Flex>
                  <Divider size={"4xl"} colorScheme={"blackAlpha"} />
                  <Flex
                    h={"10%"}
                    w={"100%"}
                    pr={3}
                    pt={3}
                    justifyContent={"flex-end"}
                  >
                    <Button
                      colorScheme="teal"
                      size="md"
                      onClick={() => setCurrentStep(2)}
                    >
                      Launch Task
                    </Button>
                  </Flex>
                </>
              )}
            </Flex>
          </Flex>
        )}

        {currentStep === 2 && (
          <Flex flexDirection={"row"} w={"50vw"} m={10}>
            {/* Left Side (Task Details) */}
            <Flex
              borderRadius="20px"
              borderWidth={5}
              borderColor="#001130"
              bgColor={"#00224D"}
              sx={{
                boxShadow: "-2px 1px 20px 10px rgba(12, 143, 148, 1)",
              }}
              flex={3}
              justifyContent={"center"}
              alignItems={"center"}
              flexDirection={"column"}
              bg={"white"}
              opacity={0.1}
            >
              {selectedTask && (
                <>
                  <Flex
                    flex={1}
                    alignItems={"center"}
                    justifyContent={"center"}
                  >
                    <Image
                      w={"100%"}
                      h={"50%"}
                      bg={"white"}
                      src={selectedTask.image_path}
                      alt={selectedTask.title}
                      borderRadius="10px"
                      mb={4}
                    />
                  </Flex>
                  <Divider
                    borderColor={"blackAlpha.500"}
                    borderWidth={2}
                    my={4}
                  />
                </>
              )}
            </Flex>

            <Flex flex={1}></Flex>

            {/* Right Side (Customization Panel) */}
            <Flex
              flex={5}
              borderRadius="20px"
              borderWidth={5}
              borderColor="#001130"
              bgColor={"#031636"}
              flexDirection={"column"}
              sx={{
                boxShadow: "-2px 1px 20px 10px rgba(12, 143, 148, 1)",
              }}
            >
              <Flex h={"10%"} justifyContent={"center"} alignItems={"center"}>
                <Heading>Customize Task</Heading>
              </Flex>

              <Flex flex={1} flexDirection={"column"} m={5}>
                <VStack spacing={5} justifyItems={"flex-start"}>
                  <Flex w="100%" align="center">
                    <Text fontSize={"xl"} flex="1" mr={2}>
                      Task Title:
                    </Text>
                    <Input
                      flex="5"
                      disabled
                      placeholder="Task Name"
                      value={customTaskName}
                      onChange={(e) => setCustomTaskName(e.target.value)}
                      mb={4}
                    />
                  </Flex>
                  <Flex w="100%" align="center">
                    <Text fontSize={"xl"} flex="2" mr={2}>
                      Task Instructions:
                    </Text>
                    <Textarea
                      flex="5" // Fixed width
                      h="10%" // or set a fixed height
                      placeholder="Task Instructions"
                      value={customTaskInstructions}
                      onChange={(e) =>
                        setCustomTaskInstructions(e.target.value)
                      }
                      mb={4}
                      disabled
                    />{" "}
                  </Flex>
                </VStack>

                {/* Live Audio Status, Live Notifications, LED Toggle */}
                <HStack mt={10} alignItems="center" mb={4} spacing={10}>
                  <Flex>
                    <Text mr={4} fontSize={"lg"}>
                      Live Audio Status
                    </Text>
                    <Switch
                      isChecked={liveAudioStatus}
                      onChange={() => setLiveAudioStatus(!liveAudioStatus)}
                    />
                  </Flex>
                  <Flex>
                    <Text mr={4} fontSize={"lg"}>
                      Live Notifications
                    </Text>
                    <Switch
                      isChecked={liveNotifications}
                      onChange={() => setLiveNotifications(!liveNotifications)}
                    />
                  </Flex>
                  <Tooltip label="Currently not available" placement="bottom">
                    <Flex>
                      <Text mr={4} fontSize={"lg"}>
                        LED Status
                      </Text>

                      <Switch
                        isChecked={ledStatus}
                        onChange={() => setLedStatus(!ledStatus)}
                        isDisabled={true} // Disabled by default
                        colorScheme="red"
                      />
                    </Flex>
                  </Tooltip>
                </HStack>

                {/* Retry Attempts */}
                <Flex alignItems="center" mt={4}>
                  <Text mr={4} w={"35%"} fontSize={"lg"}>
                    Retry Attempts: {retryAttempts}
                  </Text>
                  <Slider
                    min={20}
                    max={30}
                    value={retryAttempts}
                    onChange={(value) => setRetryAttempts(value)}
                  >
                    <SliderTrack>
                      <SliderFilledTrack />
                    </SliderTrack>
                    <SliderThumb />
                  </Slider>
                </Flex>

                {/* Scene Description Toggle */}
                <HStack mt={8} alignItems="center">
                  <Text mr={4} fontSize={"lg"}>
                    Display Scene Description
                  </Text>
                  <Switch
                    isChecked={showSceneDescription}
                    onChange={() =>
                      setShowSceneDescription(!showSceneDescription)
                    }
                  />
                </HStack>

                {/* Conditional Rendering of Scene Description */}
                {showSceneDescription && (
                  <Text mt={3} color={"white"} fontSize={"lg"}>
                    {selectedTask?.sceneDescription ||
                      "No scene description available."}
                  </Text>
                )}
              </Flex>

              <Divider borderColor={"blackAlpha.500"} borderWidth={2} my={4} />
              <Flex
                h={"10%"}
                w={"100%"}
                pr={3}
                pt={3}
                justifyContent={"flex-end"}
              >
                <Button
                  colorScheme="blue"
                  size="md"
                  mr={3}
                  onClick={() => setCurrentStep(currentStep - 1)}
                >
                  Back
                </Button>
                <Button
                  colorScheme="teal"
                  size="md"
                  onClick={handleCustomizeTask}
                >
                  Save & Continue
                </Button>
              </Flex>
            </Flex>
          </Flex>
        )}
        {currentStep === 3 && (
          <Flex
            justifyContent={"space-between"}
            flexDirection="row"
            flex={1}
            m={10}
            p={5}
          >
            <Flex
              borderRadius="20px"
              borderWidth={5}
              borderColor="#001130"
              bgColor="#00224D"
              sx={{ boxShadow: "-2px 1px 20px 10px rgba(12, 143, 148, 1)" }}
              justifyContent="space-between"
              alignItems="center"
              flexDirection="column"
              h="100%"
              w={"20%"}
              p={2}
            >
              <Flex
                alignContent={"center"}
                justifyContent={"center"}
                h={70}
                pt={5}
                textAlign={"center"}
                w={"100%"}
              >
                <Text fontSize="4xl" mb={4} fontWeight="bold">
                  Launch Status
                </Text>
              </Flex>
              <Divider borderColor="gray.500" w="90%" my={4} />
              <VStack
                w={"100%"}
                flexDirection="column"
                alignItems="flex-start"
                p={6}
                flex={1}
                spacing={6}
              >
                <Flex flexDirection={"row"} alignItems={"center"}>
                  <Box
                    bg={"green.300"}
                    w={3}
                    h={3}
                    borderRadius={"full"}
                    mr={5}
                    boxShadow="0 0 10px green, 0 0 20px green"
                    animation="glow 1.5s infinite alternate"
                    sx={{
                      "@keyframes glow": {
                        "0%": {
                          boxShadow: "0 0 5px green, 0 0 10px green",
                        },
                        "100%": {
                          boxShadow: "0 0 15px green, 0 0 30px green",
                        },
                      },
                    }}
                  ></Box>
                  <Text fontSize="md" mt={2}>
                    <strong>Task:</strong> {selectedTask?.title}
                  </Text>
                </Flex>

                <Flex flexDirection={"row"} alignItems={"center"}>
                  <Box
                    bg={"green.300"}
                    w={3}
                    h={3}
                    borderRadius={"full"}
                    mr={5}
                    boxShadow="0 0 10px green, 0 0 20px green"
                    animation="glow 1.5s infinite alternate"
                    sx={{
                      "@keyframes glow": {
                        "0%": {
                          boxShadow: "0 0 5px green, 0 0 10px green",
                        },
                        "100%": {
                          boxShadow: "0 0 15px green, 0 0 30px green",
                        },
                      },
                    }}
                  ></Box>
                  <Text fontSize="md" mt={2}>
                    <strong>Custom Name:</strong> {customTaskName}
                  </Text>
                </Flex>

                <Flex flexDirection={"row"} alignItems={"center"}>
                  <Box
                    bg={"green.300"}
                    w={3}
                    h={3}
                    borderRadius={"full"}
                    mr={5}
                    boxShadow="0 0 10px green, 0 0 20px green"
                    animation="glow 1.5s infinite alternate"
                    sx={{
                      "@keyframes glow": {
                        "0%": {
                          boxShadow: "0 0 5px green, 0 0 10px green",
                        },
                        "100%": {
                          boxShadow: "0 0 15px green, 0 0 30px green",
                        },
                      },
                    }}
                  ></Box>
                  <Text fontSize="md" mt={2}>
                    <strong>Live Audio:</strong>{" "}
                    {liveAudioStatus ? "On" : "Off"}
                  </Text>
                </Flex>

                <Flex flexDirection={"row"} alignItems={"center"}>
                  <Box
                    bg={"green.300"}
                    w={3}
                    h={3}
                    borderRadius={"full"}
                    mr={5}
                    boxShadow="0 0 10px green, 0 0 20px green"
                    animation="glow 1.5s infinite alternate"
                    sx={{
                      "@keyframes glow": {
                        "0%": {
                          boxShadow: "0 0 5px green, 0 0 10px green",
                        },
                        "100%": {
                          boxShadow: "0 0 15px green, 0 0 30px green",
                        },
                      },
                    }}
                  ></Box>
                  <Text fontSize="md" mt={2}>
                    <strong>Live Notifications:</strong>{" "}
                    {liveNotifications ? "Enabled" : "Disabled"}
                  </Text>
                </Flex>

                <Flex flexDirection={"row"} alignItems={"center"}>
                  <Box
                    bg={"green.300"}
                    w={3}
                    h={3}
                    borderRadius={"full"}
                    mr={5}
                    boxShadow="0 0 10px green, 0 0 20px green"
                    animation="glow 1.5s infinite alternate"
                    sx={{
                      "@keyframes glow": {
                        "0%": {
                          boxShadow: "0 0 5px green, 0 0 10px green",
                        },
                        "100%": {
                          boxShadow: "0 0 15px green, 0 0 30px green",
                        },
                      },
                    }}
                  ></Box>
                  <Text fontSize="md" mt={2}>
                    <strong>Retry Attempts:</strong> {retryAttempts}
                  </Text>
                </Flex>

                <Flex flexDirection={"row"} alignItems={"center"}>
                  <Box
                    bg={"green.300"}
                    w={3}
                    h={3}
                    borderRadius={"full"}
                    mr={5}
                    boxShadow="0 0 10px green, 0 0 20px green"
                    animation="glow 1.5s infinite alternate"
                    sx={{
                      "@keyframes glow": {
                        "0%": {
                          boxShadow: "0 0 5px green, 0 0 10px green",
                        },
                        "100%": {
                          boxShadow: "0 0 15px green, 0 0 30px green",
                        },
                      },
                    }}
                  ></Box>
                  <Text fontSize="md" mt={2}>
                    <strong>LED:</strong> {ledStatus ? "On" : "Off"}
                  </Text>
                </Flex>

                <Flex flexDirection={"row"} alignItems={"center"}>
                  <Box
                    bg={"green.300"}
                    w={3}
                    h={3}
                    borderRadius={"full"}
                    mr={5}
                    boxShadow="0 0 10px green, 0 0 20px green"
                    animation="glow 1.5s infinite alternate"
                    sx={{
                      "@keyframes glow": {
                        "0%": {
                          boxShadow: "0 0 5px green, 0 0 10px green",
                        },
                        "100%": {
                          boxShadow: "0 0 15px green, 0 0 30px green",
                        },
                      },
                    }}
                  ></Box>
                  <Text fontSize="md" mt={2}>
                    <strong>Scene Description:</strong>{" "}
                    {showSceneDescription ? "Visible" : "Hidden"}
                  </Text>
                </Flex>
                <Flex flexDirection={"row"} alignItems={"center"}>
                  <Box
                    bg={"green.300"}
                    w={3}
                    h={3}
                    borderRadius={"full"}
                    mr={5}
                    boxShadow="0 0 10px green, 0 0 20px green"
                    animation="glow 1.5s infinite alternate"
                    sx={{
                      "@keyframes glow": {
                        "0%": {
                          boxShadow: "0 0 5px green, 0 0 10px green",
                        },
                        "100%": {
                          boxShadow: "0 0 15px green, 0 0 30px green",
                        },
                      },
                    }}
                  ></Box>
                  <Text fontSize="md" mt={2}>
                    <strong>Task Status:</strong> {status}
                  </Text>
                </Flex>
              </VStack>
              <Divider borderColor="gray.500" w="90%" my={4} />
              <Flex
                w={"100%"}
                h={20}
                alignItems={"center"}
                justifyContent={"center"}
              >
                <Button
                  colorScheme="teal"
                  size="lg"
                  onClick={resetLaunchState}
                  isDisabled={isLaunched}
                >
                  Go Back to Task Selection
                </Button>
              </Flex>
            </Flex>
            <Flex
              justifyContent="center"
              // alignItems="center"
              flexDirection={"column"}
              w={"50%"}
              h={"100%"}
            >
              {!isConnected && !isConnecting ? (
                <Flex
                  w="100%"
                  h="20%"
                  flexDirection="column"
                  justifyContent="center"
                  alignItems="center"
                  p={4}
                  bg="rgba(0, 0, 0, 0.7)" // Semi-transparent background
                  borderRadius="md" // Rounded corners
                  boxShadow="lg" // Shadow for depth
                >
                  <Text
                    fontSize="xl"
                    fontWeight="bold"
                    color="white" // High contrast for better visibility
                    mb={4}
                    textAlign="center"
                  >
                    Connection lost. Please reconnect.
                  </Text>

                  <Progress
                    size="lg"
                    colorScheme="teal" // Vibrant color scheme
                    isIndeterminate
                    width="80%" // Adjusted width for alignment
                    borderRadius="md" // Rounded corners for the progress bar
                    boxShadow="md" // Shadow for depth on the progress bar
                  />
                </Flex>
              ) : (
                <Flex w="100%" h="100%" flexDirection="column" p={4}>
                  <Flex
                    flex={8}
                    justifyContent={"center"}
                    alignItems={"center"}
                  >
                    <Image
                      borderWidth={5}
                      borderColor="#001130"
                      sx={
                        isLaunched && isTaskEnded
                          ? {
                              boxShadow:
                                "-2px 1px 20px 10px rgba(12, 143, 148, 1)",
                            }
                          : {
                              opacity: isLaunched ? percentage / 100 : 1, // Conditionally set opacity
                              transition: "opacity 3s ease",
                            }
                      }
                      borderRadius={!isLaunched && isTaskEnded ? "full" : 0}
                      src={
                        isLaunched && isTaskEnded
                          ? isSucceeded
                            ? "success.jpeg"
                            : "error.jpeg"
                          : "car.png"
                      }
                      w={"40vw"}
                      h={"55vh"}
                    />
                  </Flex>

                  {!isTaskEnded ? (
                    <Flex
                      flex={2}
                      justifyContent={"center"}
                      alignItems={"center"}
                      flexDir={"column"}
                    >
                      {!isLaunched ? (
                        <Flex
                          w={"100%"}
                          flexDir={"row"}
                          justifyContent={"center"}
                          alignItems={"center"}
                          mb={4}
                        >
                          <Button
                            leftIcon={<Icon as={FaRocket} />}
                            colorScheme="teal"
                            onClick={handleLaunchClick}
                          >
                            Launch
                          </Button>
                        </Flex>
                      ) : (
                        <>
                          <Flex
                            w={"100%"}
                            flexDir={"row"}
                            justifyContent={"space-between"}
                            mb={4}
                          >
                            <Text
                              fontSize="2xl"
                              fontWeight="bold"
                              textAlign="center"
                              transition="opacity 3s ease"
                            >
                              {promotionalTexts[textIndex]}
                            </Text>
                            <Text
                              fontSize="xl"
                              fontWeight="bold"
                              color="white" // High contrast for better visibility
                              mb={4}
                              textAlign="center"
                            >
                              {percentage}%
                            </Text>
                          </Flex>

                          <Progress
                            size="lg"
                            value={percentage}
                            colorScheme="teal" // Vibrant color scheme
                            width="100%" // Adjusted width for alignment
                            borderRadius="md" // Rounded corners for the progress bar
                            boxShadow="md" // Shadow for depth on the progress bar
                          />
                        </>
                      )}
                    </Flex>
                  ) : (
                    <Flex
                      flex={2}
                      justifyContent={"center"}
                      alignItems={"center"}
                      flexDir={"column"}
                    >
                      <Button
                        colorScheme={isSucceeded ? "green" : "red"}
                        size="lg"
                        onClick={() => {
                          resetLaunchState();
                        }}
                      >
                        {isSucceeded ? " Task Completed" : "Try again"}
                      </Button>
                    </Flex>
                  )}
                </Flex>
              )}
            </Flex>
            <Flex
              justifyContent="space-between"
              flexDirection={"column"}
              w={"15%"}
              h={"100%"}
            >
              <Flex
                borderRadius="20px"
                borderWidth={5}
                borderColor="#001130"
                bgColor="#00224D"
                sx={{ boxShadow: "-2px 1px 20px 10px rgba(12, 143, 148, 1)" }}
                justifyContent="center"
                alignItems="center"
                flexDirection={"column"}
                w={"100%"}
                h={"30%"}
                bg={"white"}
                opacity={selectedTask.id == 2 ? 0.8 : 0.1}
              >
                <Image
                  w={"60%"}
                  h={"80%"}
                  bg={"white"}
                  src={"bottle.jpg"}
                  alt={selectedTask.title}
                  borderRadius="10px"
                  mb={4}
                />
              </Flex>
              <Flex
                borderRadius="20px"
                borderWidth={5}
                borderColor="#001130"
                bgColor="#00224D"
                sx={{ boxShadow: "-2px 1px 20px 10px rgba(12, 143, 148, 1)" }}
                justifyContent="center"
                alignItems="center"
                flexDirection={"column"}
                w={"100%"}
                h={"30%"}
                bg={"white"}
                opacity={selectedTask.id == 3 ? 0.8 : 0.1}
              >
                <Image
                  w={"60%"}
                  h={"80%"}
                  bg={"white"}
                  src={"speedstick.PNG"}
                  alt={selectedTask.title}
                  borderRadius="10px"
                  mb={4}
                />
              </Flex>
              <Flex
                borderRadius="20px"
                borderWidth={5}
                borderColor="#001130"
                bgColor="yellow"
                sx={{ boxShadow: "-2px 1px 20px 10px rgba(12, 143, 148, 1)" }}
                justifyContent="center"
                alignItems="center"
                flexDirection={"column"}
                w={"100%"}
                h={"30%"}
                bg={"white"}
                opacity={selectedTask.id == 1 ? 0.8 : 0.1}
              >
                <Image
                  w={"60%"}
                  h={"80%"}
                  bg={"white"}
                  src={"xl.png"}
                  alt={selectedTask.title}
                  borderRadius="10px"
                  mb={4}
                />
              </Flex>
            </Flex>
          </Flex>
        )}
      </Flex>
      <Flex
        h={"10vh"}
        w={"100%"}
        alignItems={"center"}
        justifyContent={"center"}
      >
        <CustomSteps
          currentStep={currentStep}
          steps={[
            {
              title: "Choose Task",
              description:
                "Choose an existing task or decide to create a new task.",
            },
            {
              title: "Customize Task",
              description: "Customize the task according to your needs.",
            },
            {
              title: "Launch Task",
              description: "Launch the task after finalizing all details.",
            },
          ]}
        />
      </Flex>
    </Flex>
  );
};

export default Launch;
