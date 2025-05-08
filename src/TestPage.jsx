import React, { useState, useEffect } from "react";
import { ref, set, onValue } from "firebase/database";
import { database } from "./firebaseConfig"; // Import firebase config

const TestPage = () => {
  const [vehicleData, setVehicleData] = useState({
    rpm: 0,
    speed: 0,
    batteryVoltage: 0,
    coolantTemp: 0,
    throttlePosition: 0
  });

  // Simulate OBD-II sensor data
  const simulateOBD2Data = () => {
    const rpm = Math.floor(Math.random() * 8000); // Simulated RPM value between 0 and 8000
    const speed = Math.floor(Math.random() * 180); // Simulated speed value between 0 and 180 km/h
    const batteryVoltage = (Math.random() * 1.5 + 12).toFixed(2); // Simulated battery voltage
    const coolantTemp = Math.floor(Math.random() * 100); // Simulated coolant temperature
    const throttlePosition = Math.floor(Math.random() * 100); // Simulated throttle position (0-100%)

    return {
      rpm,
      speed,
      batteryVoltage,
      coolantTemp,
      throttlePosition
    };
  };

  // Function to send simulated data to Firebase
  const sendSimulatedDataToFirebase = () => {
    const simulatedData = simulateOBD2Data();
    set(ref(database, "vehicleData"), simulatedData)
      .then(() => {
        console.log("Data sent to Firebase successfully");
      })
      .catch((error) => {
        console.error("Error sending data to Firebase:", error);
      });
  };

  // Function to read real-time data from Firebase
  const readDataFromFirebase = () => {
    const vehicleDataRef = ref(database, "vehicleData");
    onValue(vehicleDataRef, (snapshot) => {
      const data = snapshot.val();
      if (data) {
        setVehicleData({
          rpm: data.rpm,
          speed: data.speed,
          batteryVoltage: data.batteryVoltage,
          coolantTemp: data.coolantTemp,
          throttlePosition: data.throttlePosition
        });
      }
    });
  };

  // Call readDataFromFirebase when the component mounts
  useEffect(() => {
    readDataFromFirebase();
  }, []);

  return (
    <div>
      <h1>Vehicle Data</h1>
      <div>
        <h2>RPM: {vehicleData.rpm}</h2>
        <h2>Speed: {vehicleData.speed} km/h</h2>
        <h2>Battery Voltage: {vehicleData.batteryVoltage} V</h2>
        <h2>Coolant Temp: {vehicleData.coolantTemp} °C</h2>
        <h2>Throttle Position: {vehicleData.throttlePosition} %</h2>
      </div>
      <button onClick={sendSimulatedDataToFirebase}>Send Simulated Data</button>
    </div>
  );
};

export default TestPage;
