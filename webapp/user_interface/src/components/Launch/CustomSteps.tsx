import React from "react";
import {
  Step,
  StepDescription,
  StepIcon,
  StepIndicator,
  StepNumber,
  StepSeparator,
  StepStatus,
  Stepper,
  Tooltip,
  VStack,
} from "@chakra-ui/react";

interface CustomStepsProps {
  steps: {
    title: string;
    description: string;
  }[];
  currentStep: number;
}

const CustomSteps: React.FC<CustomStepsProps> = ({ steps, currentStep }) => {
  return (
    <Stepper
      size="3xl"
      index={currentStep}
      orientation="horizontal"
      w="50%"
      colorScheme="teal"
    >
      {steps.map((step, index) => (
        <Step key={index}>
          <StepIndicator boxSize="60px">
            <StepStatus
              complete={<StepIcon boxSize={4} />}
              incomplete={<StepNumber>{index + 1}</StepNumber>}
              active={<StepNumber>{index + 1}</StepNumber>}
            />
          </StepIndicator>
          <VStack spacing={1}>
            <Tooltip label={step.description} placement="top" hasArrow>
              <StepDescription>{step.title}</StepDescription>
            </Tooltip>
          </VStack>
          {index < steps.length - 1 && <StepSeparator />}
        </Step>
      ))}
    </Stepper>
  );
};

export default CustomSteps;
