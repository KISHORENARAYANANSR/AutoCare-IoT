import pandas as pd
from sklearn.ensemble import IsolationForest # type: ignore

# Example training data
data = [
    {'speed': 60, 'battery_voltage': 400, 'soc': 50, 'motor_temp': 70, 'battery_health': 80, 'regen_braking': False},
    {'speed': 100, 'battery_voltage': 410, 'soc': 60, 'motor_temp': 80, 'battery_health': 85, 'regen_braking': True},
    {'speed': 20, 'battery_voltage': 395, 'soc': 40, 'motor_temp': 50, 'battery_health': 90, 'regen_braking': False},
    {'speed': 90, 'battery_voltage': 405, 'soc': 70, 'motor_temp': 60, 'battery_health': 75, 'regen_braking': True},
]

# Convert data to DataFrame
df = pd.DataFrame(data)

# Drop non-numeric features (if necessary)
df = df.drop(columns=['regen_braking'])

# Initialize and train the model
model = IsolationForest()
model.fit(df)

# Save the trained model
import joblib # type: ignore
joblib.dump(model, "C:\\PROJECT\\AutoCare IoT\\model.pkl")

print("Model trained and saved successfully!")
