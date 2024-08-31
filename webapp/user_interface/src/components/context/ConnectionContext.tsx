import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useRef,
} from "react";

interface ConnectionContextProps {
  currentIpAddress: string;
  isConnected: boolean;
  isConnecting: boolean;
  setCurrentIpAddress: (ip: string) => void;
  handleReconnect: () => void;
}

const ConnectionContext = createContext<ConnectionContextProps | undefined>(
  undefined
);

export const useConnection = () => {
  const context = useContext(ConnectionContext);
  if (!context) {
    throw new Error("useConnection must be used within a ConnectionProvider");
  }
  return context;
};

export const ConnectionProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [currentIpAddress, setCurrentIpAddress] = useState<string>(() => {
    return localStorage.getItem("currentIpAddress") || "";
  });
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [isConnecting, setIsConnecting] = useState<boolean>(false);

  const checkAttemptsRef = useRef(0);
  const intervalIdRef = useRef<number | undefined>(undefined);

  const fetchIpAddress = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8080/car/currentAddress");
      if (response.ok) {
        const data = await response.json();
        return data;
      } else {
        console.error("Failed to fetch IP address:", response.statusText);
        return null;
      }
    } catch (error) {
      console.error("Error fetching IP address:", error);
      return null;
    }
  };

  useEffect(() => {
    const getIpAddress = async () => {
      const data = await fetchIpAddress();
      if (data && data.current_ip) {
        setCurrentIpAddress(data.current_ip);
        localStorage.setItem("currentIpAddress", data.current_ip);
      }
    };
    getIpAddress();
  }, []);

  useEffect(() => {
    const handleConnectionCheck = async () => {
      setIsConnecting(true);
      setIsConnected(false);

      if (currentIpAddress !== "") {
        checkAttemptsRef.current = 0;
        const response = await fetchIpAddress();
        if (response && response.current_ip !== currentIpAddress) {
          await updateIpAddress(currentIpAddress);
        }

        startConnectionCheck();
      }
    };

    handleConnectionCheck();

    return () => {
      stopConnectionCheck();
    };
  }, [currentIpAddress]);

  const updateIpAddress = async (newIp: string) => {
    try {
      const response = await fetch("http://127.0.0.1:8080/car/updateAddress", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ new_ip: newIp }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log("IP address updated successfully:", data.new_ip);
      } else {
        console.error("Failed to update IP address:", response.statusText);
      }
    } catch (error) {
      console.error("Error updating IP address:", error);
    }
  };

  const startConnectionCheck = () => {
    stopConnectionCheck();

    intervalIdRef.current = window.setInterval(() => {
      checkConnection();
    }, 10000);
  };

  const stopConnectionCheck = () => {
    if (intervalIdRef.current !== undefined) {
      clearInterval(intervalIdRef.current);
    }
  };

  const checkConnection = async () => {
    let connected = false;

    try {
      const healthResponse = await fetch("http://127.0.0.1:8080/health");
      if (healthResponse.ok) {
        const healthData = await healthResponse.json();
        if (healthData.status === "ok") {
          connected = true;
        }
      }
    } catch (error) {
      console.error("Error checking connection:", error);
    }

    setIsConnecting(false);
    setIsConnected(connected);

    if (!connected) {
      checkAttemptsRef.current += 1;
    } else {
      checkAttemptsRef.current = 0;
    }

    if (checkAttemptsRef.current >= 4) {
      stopConnectionCheck();
    }
  };

  const handleReconnect = () => {
    checkAttemptsRef.current = 0;
    setIsConnecting(true);
    startConnectionCheck();
  };

  return (
    <ConnectionContext.Provider
      value={{
        currentIpAddress,
        isConnected,
        isConnecting,
        setCurrentIpAddress,
        handleReconnect,
      }}
    >
      {children}
    </ConnectionContext.Provider>
  );
};
