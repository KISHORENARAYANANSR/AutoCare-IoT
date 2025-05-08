import firebase_admin # type: ignore
from firebase_admin import credentials, db # type: ignore
import pandas as pd
from sklearn.ensemble import IsolationForest # type: ignore
import pickle

# Initialize Firebase
cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'Your Firebase Database URL'
    # Replace with your actual Firebase database URL
})

# Firebase reference
ref = db.reference("/evData")

# Extract historical data
data = ref.get()  # Get all the data from Firebase

# Convert data to DataFrame for easier manipulation
df = pd.DataFrame(data).T  # Transpose to make each entry a row

# Use pandas' to_datetime with errors='coerce' to handle microseconds
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Prepare the features for the model (e.g., excluding timestamp)
features = df[['speed', 'battery_voltage', 'soc', 'motor_temp', 'battery_health']]

# Initialize the Isolation Forest model
model = IsolationForest(contamination=0.05)  # 5% of data are anomalies

# Fit the model
model.fit(features)

# Save the trained model to a file
with open('anomaly_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

print("Model trained and saved successfully.")
