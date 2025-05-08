  # ⚡ AutoCare IoT – EV Live Health Monitoring Dashboard

  AutoCare IoT is an advanced real-time Electric Vehicle (EV) health monitoring system designed to display live diagnostics, detect anomalies using ML (Isolation Forest), and assist in predictive maintenance. It uses OBD-II data, Firebase integration, and a beautiful React-based dashboard UI.

![Screenshot 2025-05-08 202206](https://github.com/user-attachments/assets/011c4473-230e-44d5-94dc-5a877994f8c8)

  ---

  ## 🚘 Real-Time Dashboard Parameters Displayed

  | Parameter            | Description                            |
  |----------------------|----------------------------------------|
  | 🚗 Speed              | Vehicle speed in km/h                 |
  | 🔋 Battery Voltage    | Current voltage of EV battery (V)     |
  | ⚡ SoC (%)            | State of Charge (Battery Level)       |
  | 🌡️ Motor Temp        | Motor temperature in °C               |
  | 🛠️ Battery Health     | Battery condition (%)                 |
  | 🔁 Regen Braking      | Regenerative braking status (ON/OFF)  |
  | ❗ DTC Codes          | Active Diagnostic Trouble Codes       |

  All parameters are updated in real time with a dynamic line graph for trend analysis.

  ---

  ## 📊 Anomaly Detection (ML-Based)

  AutoCare IoT integrates an **Isolation Forest** model (unsupervised ML) to detect anomalies like:

  - Abnormal battery voltage drops
  - Unexpected high speed spikes
  - High motor temperatures
  - Low battery health trends

  ✅ If no anomaly is detected:  
  `Anomaly Status: No ✅`  
  🔔 If an anomaly is detected:  
  `Anomaly Status: Yes ❗` (Dashboard turns alert color & triggers beep)

  ---

  ## 📨 Emergency SMS Alert Feature

  In case of a critical anomaly or accident-like behavior, the system is capable of sending **real-time SMS alerts** using an integrated SMS API.

  **Features:**
  - Sends an SMS alert to a predefined emergency contact
  - Message includes timestamp, and issue detected
  - Useful for breakdown, overheating, or battery failure scenarios

  > Example SMS:  
  > `Alert: EV anomaly detected in your Vehicle at 2025-05-08 20:12:45. Check motor temperature and battery health.`

  ---

  ## 📈 Real-Time EV Data Graph

  The dashboard visualizes live values of:

  - Speed  
  - Battery Voltage  
  - SoC (%)  
  - Motor Temperature  
  - Battery Health  

  All values are plotted against timestamps to track fluctuations and spot issues early.

  ---

  ## 🛠️ Maintenance Indicator

  At the bottom of the dashboard:

  - ✅ **No Anomaly Detected:** Indicates normal vehicle operation  
  - 🛠️ **Maintenance Status:** Displays `All Systems Normal` unless an issue arises

  ---

  ## 🔧 Tech Stack

  | Component        | Technology          |
  |------------------|---------------------|
  | Frontend         | React.js (App.jsx)  |
  | Backend/Cloud    | Firebase Realtime DB |
  | ML Model         | Python + scikit-learn |
  | Communication    | WebSocket (or Firebase SDK) |
  | Data Source      | OBD-II Simulator (pyOBD)|
  | SMS Alerts       | Twilio |

  ---

## 🚀 How to Run the Project

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/AutoCare-IoT.git
   cd AutoCare-IoT
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Set Up Firebase**
   - Create a Firebase project
   - Enable Realtime Database
   - Add config details to `firebase.js`

4. **Run the React Frontend**
   ```bash
   npm start
   ```

5. **Run ML Backend**
   ```bash
   python ml/train_model.py
   python ml/realtime_anomaly_detector.py
   ```

6. **Enable SMS Alerts (Optional)**
   ```bash
   python alerts/sms_alert.py
   ```

7. **Stream OBD-II Data**
   - Use an OBD-II emulator like pyOBD 
   - Ensure values sync to Firebase in real time

---

## 🔮 Future Enhancements

- 📱 React Native Mobile App  
- 📉 Exportable vehicle logs  
- 📦 Integration with real OBD-II dongles  
- 🧠 More ML models for behavior classification  
- 🛰️ OTA updates for rule engine  
- 📡 V2V Integration & ambulance detection module

---


## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

> 🚀 Live smarter, drive safer — AutoCare IoT
