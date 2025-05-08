import pandas as pd
import joblib # type: ignore
from firebase_update import update_anomaly_status  # type: ignore # Import the function to update Firebase

# Load the trained model
model = joblib.load("path/to/your/model.pkl")

def predict_anomaly(ev_data):
    """
    Function to predict anomalies using the trained model
    """
    # Prepare the data for prediction by removing the 'timestamp' and 'dtc' columns
    df = pd.DataFrame([ev_data])
    df = df.drop(columns=['timestamp', 'dtc'])  # Remove non-numeric columns if present

    # Make the prediction
    prediction = model.predict(df)

    # Check if prediction is an anomaly
    if prediction == -1:
        update_anomaly_status('Anomaly')  # Update Firebase with anomaly status
        return 'Anomaly Detected'
    else:
        update_anomaly_status('No anomaly')  # Update Firebase with no anomaly status
        return 'No Anomaly Detected'

def process_ev_data(ev_data):
    """
    Function to process incoming EV data and detect anomalies
    """
    result = predict_anomaly(ev_data)
    print(result)  # Log or display the result of anomaly prediction

# Example: An EV data point that you receive from your system
ev_data_example = {
    'speed': 500,
    'battery_voltage': 150,
    'soc': 10,
    'motor_temp': 150,
    'battery_health': 50,
    'regen_braking': False,
    'dtc': 'BMS_ERROR',
    'timestamp': '2025-05-06T21:35:00'
}

# Process the EV data and check for anomalies
process_ev_data(ev_data_example)
