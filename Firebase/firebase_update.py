import firebase_admin # type: ignore
from firebase_admin import credentials, db # type: ignore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("C:\PROJECT\AutoCare IoT\src\firebaseConfig.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'your_firebase_database_url'  # Replace with your actual Firebase database URL
})

def update_anomaly_status(anomaly_status):
    ref = db.reference('evData')
    ref.update({
        'anomaly': anomaly_status
    })
    print(f"Anomaly status updated to: {anomaly_status}")
