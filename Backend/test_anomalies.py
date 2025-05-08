import pandas as pd
from sklearn.ensemble import IsolationForest # type: ignore
import joblib # type: ignore

# Load the trained model (if it already exists)
try:
    model = joblib.load("C:\\PROJECT\\AutoCare IoT\\model.pkl")
except FileNotFoundError:
    print("Model file not found. Please train the model first.")
    exit()

# Extreme test data
extreme_data = [
    {'speed': 500, 'battery_voltage': 150, 'soc': 10, 'motor_temp': 150, 'battery_health': 50, 'regen_braking': False, 'dtc': 'BMS_ERROR', 'timestamp': '2025-05-06T21:35:00'},
    {'speed': 0, 'battery_voltage': 420, 'soc': 100, 'motor_temp': 20, 'battery_health': 100, 'regen_braking': False, 'dtc': '', 'timestamp': '2025-05-06T21:35:05'},
    {'speed': 300, 'battery_voltage': 100, 'soc': 5, 'motor_temp': 120, 'battery_health': 30, 'regen_braking': True, 'dtc': 'OVERHEAT', 'timestamp': '2025-05-06T21:35:10'},
    {'speed': 200, 'battery_voltage': 350, 'soc': 25, 'motor_temp': 80, 'battery_health': 60, 'regen_braking': True, 'dtc': '', 'timestamp': '2025-05-06T21:35:15'}
]

# Convert test data to DataFrame
df_extreme = pd.DataFrame(extreme_data)

# Remove the 'timestamp' and 'dtc' columns, and the 'regen_braking' column if needed
df_extreme = df_extreme.drop(columns=['timestamp', 'dtc', 'regen_braking'])

# Make predictions
predictions = model.predict(df_extreme)

# Display results
for i, prediction in enumerate(predictions):
    print(f"Timestamp: {extreme_data[i]['timestamp']} - EV Data: {extreme_data[i]} - {'Anomaly' if prediction == -1 else 'No anomaly'}")
