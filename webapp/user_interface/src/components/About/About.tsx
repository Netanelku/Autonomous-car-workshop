import React from "react";
import {
  Box,
  Heading,
  Text,
  VStack,
  Flex,
  useColorModeValue,
  Divider,
} from "@chakra-ui/react";
import backgroundImage from "../../images/background1.jpg"; // Adjust the path as needed

const About: React.FC = () => {
  const overlayColor = useColorModeValue(
    "rgba(0, 0, 0, 0.7)",
    "rgba(255, 255, 255, 0.2)"
  );
  const textColor = useColorModeValue("white", "teal.300");

  return (
    <Flex
      flex={1}
      direction="column"
      bgImage={`url(${backgroundImage})`}
      bgSize="cover"
      bgPosition="center"
      bgRepeat="no-repeat"
      color={textColor}
      justifyContent="center"
      alignItems="center"
      position="relative"
      overflow="hidden"
      p={10}
    >
      {/* Overlay for better text readability */}
      <Box
        position="absolute"
        top={0}
        left={0}
        width="100%"
        height="100%"
        bg={overlayColor}
      />

      {/* Pinned title */}
      <Flex
        position="sticky"
        top={0}
        // bg="rgba(0, 0, 0, 0.8)"
        p={4}
        zIndex={1}
        mb={8} // Margin-bottom to separate from content
        justifyContent={"center"}
      >
        <Heading as="h1" size="3xl" color="teal.300">
          About Smart Retrieval Autonomous Car
        </Heading>
      </Flex>

      <VStack
        spacing={8} // Adjusted spacing for better readability
        p={6}
        zIndex={1}
        w={"80vw"}
        // maxW={"900px"}
        h={"70vh"} // Changed from fixed height to auto to fit content
        overflowY={"auto"} // Use auto to show scroll bar only if needed
        borderRadius="xl"
        boxShadow="lg"
        bg="rgba(0, 0, 0, 0.8)"
        align="start"
        m={5}
      >
        <Box>
          <Heading as="h2" size="xl" color="teal.200" mb={6}>
            Introduction
          </Heading>
          <Text fontSize="lg" mb={4} color="gray.200">
            We propose the creation of a Smart Retrieval Autonomous Car. This
            innovative vehicle leverages state-of-the-art technology to enhance
            operational efficiency in item retrieval tasks. It is equipped with
            cutting-edge features designed to streamline the retrieval process
            and ensure optimal performance in various environments.
          </Text>
          <Text fontSize="lg" mb={4} color="gray.200">
            This vehicle is designed for swift item retrieval within designated
            areas, offering significant advantages over traditional methods. By
            incorporating advanced sensors and algorithms, the car can navigate
            complex environments and retrieve items with high precision and
            speed, making it an invaluable tool for various industries.
          </Text>
        </Box>
        <Divider borderColor="teal.500" />

        <Box>
          <Heading as="h2" size="xl" color="teal.200" mb={4}>
            Key Features
          </Heading>
          <Text fontSize="lg" mb={3} color="gray.200">
            It integrates features like wireless WiFi remote control, allowing
            users to operate the vehicle from a distance with ease. This feature
            enhances flexibility and convenience, enabling users to control the
            car's movements and actions without being physically present.
          </Text>
          <Text fontSize="lg" mb={3} color="gray.200">
            A mobile camera is included for visual identification, which enables
            the car to recognize and locate items based on visual cues. This
            capability is particularly useful in environments where items may be
            placed in various locations or configurations, ensuring accurate and
            efficient retrieval.
          </Text>
          <Text fontSize="lg" mb={3} color="gray.200">
            Additionally, the vehicle is equipped with real-time tracking and
            data analysis tools, providing valuable insights into its
            performance and the retrieval process. These tools allow for
            continuous optimization and adjustment, ensuring the highest level
            of efficiency and effectiveness.
          </Text>
        </Box>

        <Divider borderColor="teal.500" />

        <Box>
          <Heading as="h2" size="xl" color="teal.200" mb={4}>
            Purpose and Goal
          </Heading>
          <Text fontSize="lg" mb={3} color="gray.200">
            The primary goal is to develop an adaptable autonomous car that can
            seamlessly integrate into various operational environments. This
            adaptability ensures that the car can meet the specific needs and
            challenges of different tasks and settings, making it a versatile
            and valuable asset.
          </Text>
          <Text fontSize="lg" mb={3} color="gray.200">
            It autonomously identifies and retrieves items guided by remote
            visual commands, reducing the need for manual intervention and
            minimizing the potential for errors. This level of automation not
            only enhances efficiency but also improves overall productivity and
            accuracy.
          </Text>
          <Text fontSize="lg" mb={3} color="gray.200">
            By leveraging advanced technologies and sophisticated algorithms,
            the car is capable of performing complex retrieval tasks with ease,
            making it an ideal solution for a wide range of applications, from
            industrial settings to research facilities and beyond.
          </Text>
        </Box>

        <Divider borderColor="teal.500" />

        <Box>
          <Heading as="h2" size="xl" color="teal.200" mb={4}>
            Innovation
          </Heading>
          <Text fontSize="lg" mb={3} color="gray.200">
            This innovative solution streamlines the retrieval process by
            incorporating the latest advancements in technology and automation.
            The car's design focuses on enhancing operational efficiency,
            reducing manual effort, and providing a reliable method for locating
            and retrieving specific items.
          </Text>
          <Text fontSize="lg" mb={3} color="gray.200">
            It offers a reliable and efficient method for locating and
            recovering specific items, making it an essential tool for various
            industries. The integration of advanced sensors, real-time tracking,
            and data analysis capabilities ensures that the car operates with
            precision and effectiveness, even in complex environments.
          </Text>
          <Text fontSize="lg" mb={3} color="gray.200">
            The innovative approach to item retrieval not only improves
            productivity but also sets a new standard for automation and
            efficiency, positioning the car as a leading solution in the field
            of autonomous systems.
          </Text>
        </Box>

        <Divider borderColor="teal.500" />

        <Box>
          <Heading as="h2" size="xl" color="teal.200" mb={4}>
            Advanced Technologies
          </Heading>
          <Text fontSize="lg" mb={3} color="gray.200">
            Equipped with advanced technologies, this autonomous car operates in
            various environments with ease. The incorporation of sophisticated
            sensors and algorithms allows the car to adapt to different
            conditions and perform tasks efficiently, regardless of the
            complexity of the environment.
          </Text>
          <Text fontSize="lg" mb={3} color="gray.200">
            WiFi connectivity and visual recognition ensure versatile use,
            providing users with the flexibility to control and monitor the car
            from a distance. These features enhance the car's functionality and
            usability, making it a valuable tool for a wide range of
            applications.
          </Text>
          <Text fontSize="lg" mb={3} color="gray.200">
            The robust build of the car ensures durability during tasks, making
            it an essential asset for demanding environments. Its construction
            is designed to withstand various conditions and challenges, ensuring
            reliable performance and longevity.
          </Text>
        </Box>

        <Divider borderColor="teal.500" />

        <Box>
          <Heading as="h2" size="xl" color="teal.200" mb={4}>
            Future of Automation
          </Heading>
          <Text fontSize="lg" mb={3} color="gray.200">
            This autonomous car represents the future of automation, offering a
            glimpse into the potential of advanced robotic systems. Its design
            and functionality reflect the latest trends and innovations in
            automation technology, setting a new standard for future
            developments.
          </Text>
          <Text fontSize="lg" mb={3} color="gray.200">
            It simplifies complex tasks, reduces human effort, and increases
            efficiency, making it a valuable asset for various industries. The
            car's ability to perform tasks autonomously with precision and
            reliability highlights its potential to revolutionize traditional
            methods and practices.
          </Text>
          <Text fontSize="lg" mb={3} color="gray.200">
            The ongoing advancements in automation technology will continue to
            drive innovation and improvement, and this autonomous car is a
            testament to the possibilities and opportunities that lie ahead in
            the field of robotics and automation.
          </Text>
        </Box>

        <Divider borderColor="teal.500" />

        <Box>
          <Heading as="h2" size="xl" color="teal.200" mb={4}>
            Conclusion
          </Heading>
          <Text fontSize="lg" mb={3} color="gray.200">
            Our initiative is a commitment to creating an effective robotic
            system that meets the needs of various industries and applications.
            The Smart Retrieval Autonomous Car represents a significant step
            forward in automation technology, offering a solution that is both
            innovative and practical.
          </Text>
          <Text fontSize="lg" mb={3} color="gray.200">
            The car's advanced features and capabilities make it a valuable tool
            for tasks requiring precise item identification and retrieval. Its
            design reflects our dedication to pushing the boundaries of
            technology and providing a solution that enhances efficiency and
            productivity.
          </Text>
          <Text fontSize="lg" mb={3} color="gray.200">
            As we continue to develop and refine our robotic systems, we are
            committed to delivering solutions that meet the highest standards of
            performance and reliability. The Smart Retrieval Autonomous Car is a
            testament to our vision for the future of automation and our
            commitment to excellence.
          </Text>
        </Box>
      </VStack>
    </Flex>
  );
};

export default About;
