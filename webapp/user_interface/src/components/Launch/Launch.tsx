import React, { useState } from "react";
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
  SliderTrack,
  SliderFilledTrack,
  SliderThumb,
  VStack,
  HStack,
  Tooltip,
} from "@chakra-ui/react";
import backgroundImage from "../../images/background.jpg"; // Adjust the path as needed
import CustomSteps from "./CustomSteps";
import tasks from "./tasks.json"; // Importing the JSON file

const Launch: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [selectedTask, setSelectedTask] = useState<any>(null);
  const [customTaskName, setCustomTaskName] = useState("");
  const [customTaskInstructions, setCustomTaskInstructions] = useState("");
  const [liveAudioStatus, setLiveAudioStatus] = useState(false);
  const [liveNotifications, setLiveNotifications] = useState(true);
  const [retryAttempts, setRetryAttempts] = useState(20);
  const [ledStatus, setLedStatus] = useState(false);
  const [showSceneDescription, setShowSceneDescription] = useState(true);
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
    setCurrentStep(3); // Move to the next step
  };

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
                  <Input
                    disabled
                    placeholder="Task Name"
                    value={customTaskName}
                    onChange={(e) => setCustomTaskName(e.target.value)}
                    mb={4}
                  />
                  <Textarea
                    placeholder="Task Instructions"
                    value={customTaskInstructions}
                    onChange={(e) => setCustomTaskInstructions(e.target.value)}
                    mb={4}
                    disabled
                  />
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
                  <Flex>
                    <Text mr={4} fontSize={"lg"}>
                      LED Status
                    </Text>
                    <Tooltip label="Currently not available" placement="bottom">
                      <Switch
                        isChecked={ledStatus}
                        onChange={() => setLedStatus(!ledStatus)}
                        isDisabled={true} // Disabled by default
                        colorScheme="red"
                      />
                    </Tooltip>
                  </Flex>
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
              alignItems={"center"}
              justifyContent={"center"}
            >
              <Text fontSize={"2xl"} mb={4}>
                Task Ready to Launch
              </Text>
              <Button
                colorScheme="teal"
                size="lg"
                onClick={() => console.log("Task Launched")}
              >
                Launch Task
              </Button>
            </Flex>
            <Flex flex={1}></Flex>
            <Flex
              borderRadius="20px"
              borderWidth={5}
              borderColor="#001130"
              bgColor={"#00224D"}
              sx={{
                boxShadow: "-2px 1px 20px 10px rgba(12, 143, 148, 1)",
              }}
              flex={5}
              justifyContent={"center"}
              alignItems={"center"}
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
                      h={"50%"}
                      bg={"white"}
                      src={selectedTask.image_path}
                      alt={selectedTask.title}
                      borderRadius="10px"
                      mb={4}
                    />
                  </Flex>
                  <Divider size={"4xl"} colorScheme={"blackAlpha"} />
                </>
              )}
            </Flex>
          </Flex>
        )}
      </Flex>
      <Flex
        h={"20vh"}
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
