import random
import time
import pandas as pd
from sklearn.ensemble import IsolationForest  # type: ignore
import pickle
from datetime import datetime

# Firebase Admin SDK
import firebase_admin  # type: ignore
from firebase_admin import credentials, db  # type: ignore

# Twilio API for SMS
from twilio.rest import Client  # type: ignore

# Load Firebase credentials and initialize
cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "Your Firebase Database URL"
})

# Load the trained anomaly detection model
with open('anomaly_model.pkl', 'rb') as f:
    model = pickle.load(f)

print("Trained model feature names: ", model.feature_names_in_)

# Twilio credentials (replace with your actual credentials)
TWILIO_PHONE_NUMBER = ''
TO_PHONE_NUMBER = ''
TWILIO_ACCOUNT_SID = ''
TWILIO_AUTH_TOKEN = ''

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Initial sensor values
current_values = {
    "speed": 0,
    "battery_voltage": 350.0,
    "soc": 80,
    "motor_temp": 50,
    "battery_health": 90,
    "regen_braking": False,
    "dtc": "",
    "maintenance_status": "Normal"
}

# Force error only once
force_error_once = True

# Smooth transition function
def smooth_value(current, target, inc_step=10, dec_step=3):
    if current < target:
        return min(current + inc_step, target)
    elif current > target:
        return max(current - dec_step, target)
    return current

# Generate realistic EV data
def generate_ev_data():
    global current_values, force_error_once

    target_values = {
        "speed": random.randint(20, 160),
        "battery_voltage": round(random.uniform(310, 410), 2),
        "soc": random.randint(60, 100),
        "motor_temp": random.randint(40, 90),
        "battery_health": random.randint(75, 100),
        "regen_braking": random.choice([True, False]),
    }

    current_values["speed"] = smooth_value(current_values["speed"], target_values["speed"], inc_step=10, dec_step=3)
    current_values["battery_voltage"] = smooth_value(current_values["battery_voltage"], target_values["battery_voltage"], inc_step=1.5, dec_step=1.5)
    current_values["soc"] = smooth_value(current_values["soc"], target_values["soc"], inc_step=1, dec_step=1)
    current_values["motor_temp"] = smooth_value(current_values["motor_temp"], target_values["motor_temp"], inc_step=1.5, dec_step=1.5)
    current_values["battery_health"] = smooth_value(current_values["battery_health"], target_values["battery_health"], inc_step=1, dec_step=1)
    current_values["regen_braking"] = target_values["regen_braking"]

    if force_error_once:
        current_values["soc"] = 15                # LOW_SOC
        current_values["motor_temp"] = 95         # OVERTEMP
        current_values["battery_voltage"] = 418   # BMS_ERROR
        current_values["battery_health"] = 75     # INVERTER_FAULT
        force_error_once = False

    if current_values["speed"] > 140:
        current_values["motor_temp"] += 2

    current_values["motor_temp"] = min(current_values["motor_temp"], 110)

    # Detect DTCs
    dtc_errors = []
    if current_values["soc"] < 20:
        dtc_errors.append("LOW_SOC")
    if current_values["motor_temp"] > 85:
        dtc_errors.append("OVERTEMP")
    if current_values["battery_voltage"] < 320 or current_values["battery_voltage"] > 415:
        dtc_errors.append("BMS_ERROR")
    if current_values["battery_health"] < 80:
        dtc_errors.append("INVERTER_FAULT")

    current_values["dtc"] = random.choice(dtc_errors) if dtc_errors else ""

    if "OVERTEMP" in dtc_errors:
        current_values["maintenance_status"] = "Check Motor Cooling System"
    elif "LOW_SOC" in dtc_errors:
        current_values["maintenance_status"] = "Recharge Battery Immediately"
    elif "BMS_ERROR" in dtc_errors:
        current_values["maintenance_status"] = "Battery Management System Fault"
    elif "INVERTER_FAULT" in dtc_errors:
        current_values["maintenance_status"] = "Check Inverter and Wiring"
    else:
        current_values["maintenance_status"] = "Normal"

    return current_values.copy()

# DTC descriptions for dynamic SMS
DTC_MESSAGES = {
    "OVERTEMP": "⚠️ Overheating detected! Motor temperature is too high. Please check cooling system.",
    "LOW_SOC": "⚠️ Battery SOC is critically low. Recharge immediately to avoid breakdown.",
    "BMS_ERROR": "⚠️ Battery Management System fault detected. Check battery voltage range.",
    "INVERTER_FAULT": "⚠️ Inverter or powertrain system fault. Check wiring or controller.",
}

# SMS alert function
def send_sms(dtc_code, timestamp, maintenance_status):
    description = DTC_MESSAGES.get(dtc_code, "⚠️ Unknown DTC code detected.")
    message = (
        f"{description}\n"
        f"Time: {timestamp}\n"
        f"Recommended Action: {maintenance_status}"
    )
    twilio_client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=TO_PHONE_NUMBER
    )
    print(f"SMS sent: {message}")

# Anomaly prediction
def predict_anomaly(data):
    df = pd.DataFrame([data])
    df['regen_braking'] = df['regen_braking'].astype(int)
    df['dtc'] = df['dtc'].apply(lambda x: 1 if x != "" else 0)
    df = df.drop(columns=['timestamp', 'maintenance_status'])
    df = df[model.feature_names_in_]
    return model.predict(df)

# Main loop
while True:
    data = generate_ev_data()
    timestamp = datetime.now().isoformat()
    data["timestamp"] = timestamp

    prediction = predict_anomaly(data)
    data["alert"] = True if prediction == -1 else False

    if data["dtc"]:
        send_sms(data["dtc"], timestamp, data["maintenance_status"])

    db.reference("evData").set(data)

    print(f"[{timestamp}] Sent to Firebase: {data}")
    time.sleep(0.5)
