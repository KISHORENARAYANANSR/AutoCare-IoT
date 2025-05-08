import firebase_admin # type: ignore
from firebase_admin import credentials, db # type: ignore
import csv

# Load credentials and initialize the app
cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'your_firebase_database_url'  # Replace with your actual Firebase database URL
})

# Reference to your EV data node
ref = db.reference('evData')
data = ref.get()

# Debug print to see what Firebase returned
print("📦 Raw Firebase data:\n", data)

# Check if data is valid
if not data:
    print("⚠️ No data found at 'evData' path. Please verify Firebase path.")
    exit()

# Create CSV file
with open('ev_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'speed', 'battery_voltage', 'soc', 'motor_temp', 'battery_health'])

    for key, value in data.items():
        if not isinstance(value, dict):
            print(f"⛔ Skipping invalid entry at {key}: Not a dictionary → {value}")
            continue

        writer.writerow([
            key,
            value.get('speed'),
            value.get('battery_voltage'),
            value.get('soc'),
            value.get('motor_temp'),
            value.get('battery_health')
        ])

print("✅ Data export complete. File saved as ev_data.csv")
