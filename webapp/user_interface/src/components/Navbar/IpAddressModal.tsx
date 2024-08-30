import React, { useState } from "react";
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  Button,
  Text,
  FormControl,
  FormLabel,
  Input,
  FormHelperText,
  FormErrorMessage,
} from "@chakra-ui/react";

interface IpAddressModalProps {
  currentIpAddress: string;
  setCurrentIpAddress: (ip: string) => void;
  isOpen: boolean;
  onClose: () => void;
}

const IpAddressModal: React.FC<IpAddressModalProps> = ({
  currentIpAddress,
  setCurrentIpAddress,
  isOpen,
  onClose,
}) => {
  const [input, setInput] = useState("");

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) =>
    setInput(e.target.value);

  const isValidIp = (ip: string) => {
    const ipRegex =
      /^(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$/;
    return ipRegex.test(ip);
  };
  const isSameIP = (ip: String) => {
    return ip == currentIpAddress;
  };
  const [isError, setIsError] = useState<boolean>(false);

  return (
    <Modal
      isOpen={isOpen}
      onClose={() => {
        setIsError(false);
        setInput("");
        onClose();
      }}
    >
      <ModalOverlay />
      <ModalContent>
        <ModalHeader fontSize="2xl">Connection Window</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          {currentIpAddress === "" ? (
            <Text color={"red"} fontSize="xl">
              Your car's IP address is not set.
            </Text>
          ) : (
            <Text mb="1rem" fontSize="xl">
              Your current car IP address is: {currentIpAddress}
            </Text>
          )}
          <FormControl
            isInvalid={isError && (!isValidIp(input) || isSameIP(input))}
          >
            <FormLabel fontSize="lg">IP Address</FormLabel>
            <Input type="text" value={input} onChange={handleInputChange} />

            {(() => {
              if (!isError) {
                if (currentIpAddress === "") {
                  return (
                    <FormHelperText>
                      Please insert a valid IP address
                    </FormHelperText>
                  );
                } else if (!isValidIp(input)) {
                  return (
                    <FormHelperText>
                      Please insert a valid IP address
                    </FormHelperText>
                  );
                } else if (isSameIP(input)) {
                  return (
                    <FormHelperText>
                      Please insert a different valid IP address
                    </FormHelperText>
                  );
                } else {
                  return (
                    <FormHelperText color="green">
                      IP address is valid
                    </FormHelperText>
                  );
                }
              } else if (!isValidIp(input)) {
                return (
                  <FormErrorMessage fontSize="md">
                    Valid IP address is required.
                  </FormErrorMessage>
                );
              } else if (isSameIP(input)) {
                return (
                  <FormErrorMessage>
                    Please insert a different IP address
                  </FormErrorMessage>
                );
              } else {
                return (
                  <FormHelperText color="green">
                    IP address is valid
                  </FormHelperText>
                );
              }
            })()}
          </FormControl>
        </ModalBody>
        <ModalFooter>
          <Button
            colorScheme="blue"
            mr={3}
            onClick={() => {
              setIsError(false);
              setInput("");
              onClose();
            }}
          >
            Close
          </Button>
          <Button
            colorScheme="blue"
            onClick={() => {
              if (isValidIp(input) && !isSameIP(input)) {
                setCurrentIpAddress(input);
                setIsError(false);
                onClose();
                setInput("");
              } else {
                setIsError(true);
              }
            }}
          >
            Save
          </Button>
          {/* <Button
            ml={2}
            colorScheme="green"
            onClick={handleReconnect}
            isDisabled={!isValidIp(currentIpAddress)}
          >
            Reconnect
          </Button> */}
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default IpAddressModal;
