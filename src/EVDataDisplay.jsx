import React, { useEffect, useState } from "react";
import { getDatabase, ref, onValue } from "firebase/database";
import { initializeApp } from "firebase/app";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from "recharts";

// Firebase Config
const firebaseConfig = {
  
};

const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

function EVDataDisplay() {
  const [evData, setEvData] = useState(null);
  const [graphData, setGraphData] = useState([]);

  useEffect(() => {
    const evDataRef = ref(db, "evData");
    onValue(evDataRef, (snapshot) => {
      const data = snapshot.val();
      setEvData(data);
      setGraphData(prev => {
        const newData = {
          timestamp: new Date().toLocaleTimeString(),
          ...data
        };
        return [...prev.slice(-19), newData]; // Keep last 20
      });
    });
  }, []);

  const styles = {
    body: {
      margin: 0,
      padding: 0,
      backgroundColor: "#0a192f",
      fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
      color: "#fff",
      minHeight: "100vh",
    },
    container: {
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      padding: "40px",
    },
    heading: {
      fontSize: "2.5rem",
      fontWeight: "bold",
      textAlign: "center",
      marginBottom: "30px",
      background: "linear-gradient(to right, #ff00cc, #ff0099)",
      WebkitBackgroundClip: "text",
      WebkitTextFillColor: "transparent",
    },
    cardsGrid: {
      display: "flex",
      flexWrap: "wrap",
      gap: "1.2rem",
      justifyContent: "center",
      marginBottom: "30px",
    },
    card: {
      background: "#1a2a3a",
      borderRadius: "12px",
      padding: "1rem 1.5rem",
      minWidth: "160px",
      boxShadow: "0 0 10px rgba(0, 255, 255, 0.2)",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
    },
    label: {
      fontWeight: "bold",
      marginBottom: "0.3rem",
      fontSize: "1rem"
    },
    value: {
      fontSize: "1.2rem"
    },
    alert: {
      fontWeight: "bold",
      marginTop: "20px",
    },
    alertYes: {
      color: "#ff4c4c",
    },
    alertNo: {
      color: "#00ff99",
    },
    graphTitle: {
      color: "#00e6e6",
      fontSize: "20px",
      marginTop: "20px",
      marginBottom: "10px",
    },
    graphContainer: {
      width: "100%",
      maxWidth: "1100px"
    }
  };

  const renderCards = () => {
    if (!evData) return null;
    const items = [
      { icon: "🚗", label: "Speed", value: `${evData.speed} km/h` },
      { icon: "🔋", label: "Battery Voltage", value: `${evData.battery_voltage} V` },
      { icon: "⚡", label: "SoC", value: `${evData.soc} %` },
      { icon: "🌡️", label: "Motor Temp", value: `${evData.motor_temp} °C` },
      { icon: "🔧", label: "Battery Health", value: `${evData.battery_health} %` },
      { icon: "♻️", label: "Regen Braking", value: evData.regen_braking ? "ON" : "OFF" },
      { icon: "❗", label: "DTC", value: evData.dtc || "None" },
    ];
    return (
      <div style={styles.cardsGrid}>
        {items.map((item, index) => (
          <div key={index} style={styles.card}>
            <span>{item.icon}</span>
            <span style={styles.label}>{item.label}</span>
            <span style={styles.value}>{item.value}</span>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div style={styles.body}>
      <div style={styles.container}>
        <h2 style={styles.heading}>⚡ AutoCare IoT – EV Live Dashboard</h2>
  
        {evData ? (
          <>
            {renderCards()}
            <div
              style={{
                ...styles.alert,
                ...(evData.anomaly === "Anomaly" ? styles.alertYes : styles.alertNo)
              }}
            >
              Anomaly Status: {evData.anomaly === "Anomaly" ? "Yes ⚠️" : "No ✅"}
            </div>
  

  
           
          </>
        ) : (
          <p style={{ textAlign: "center", color: "#aaa" }}>Loading vehicle data...</p>
        )}
  
        <h3 style={styles.graphTitle}>📈 Real-Time EV Data Graph</h3>
        <div style={styles.graphContainer}>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={graphData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#444" />
              <XAxis dataKey="timestamp" stroke="#ccc" />
              <YAxis stroke="#ccc" />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="speed" stroke="#00ff99" name="Speed" />
              <Line type="monotone" dataKey="battery_voltage" stroke="#ffcc00" name="Voltage" />
              <Line type="monotone" dataKey="soc" stroke="#33ccff" name="SoC (%)" />
              <Line type="monotone" dataKey="motor_temp" stroke="#ff6666" name="Motor Temp" />
              <Line type="monotone" dataKey="battery_health" stroke="#66ff66" name="Battery Health" />
            </LineChart>
          </ResponsiveContainer>
        </div>
        {/* 🔽 STATIC ALERT CARDS BELOW GRAPH 🔽 */}
<div style={{ marginTop: "30px", display: "flex", gap: "20px", justifyContent: "center", flexWrap: "wrap" }}>
  {/* Anomaly Alert Box */}
  <div
    style={{
      backgroundColor: evData?.anomaly === "Anomaly" ? "#ff1a1a" : "#1a2a3a",
      color: "white",
      fontSize: "1.2rem",
      padding: "20px 30px",
      borderRadius: "16px",
      fontWeight: "bold",
      boxShadow: evData?.anomaly === "Anomaly" ? "0 0 15px rgba(255, 0, 0, 0.6)" : "none",
      textAlign: "center",
      minWidth: "300px",
    }}
  >
    🚨 Anomaly Status: {evData?.anomaly === "Anomaly" ? "Anomaly Detected – Immediate Attention Required!" : "No Anomaly Detected ✅"}
  </div>

  {/* DTC Maintenance Box */}
  <div
    style={{
      backgroundColor: evData?.dtc === "LOW_SOC" ? "#e67300" : "#1a2a3a",
      color: "white",
      fontSize: "1.2rem",
      padding: "20px 30px",
      borderRadius: "16px",
      fontWeight: "bold",
      boxShadow: evData?.dtc === "LOW_SOC" ? "0 0 15px rgba(255, 140, 0, 0.6)" : "none",
      textAlign: "center",
      minWidth: "300px",
    }}
  >
    🛠️ Maintenance Status: {evData?.dtc === "LOW_SOC" ? "LOW SOC – Maintenance Required!" : "All Systems Normal ✅"}
  </div>
</div>
      </div>
    </div>
  );
}  

export default EVDataDisplay;
