
from flask import Flask, jsonify, request
import pandas as pd
from sklearn.ensemble import IsolationForest # type: ignore
import joblib # type: ignore

# Initialize Flask app
app = Flask(__name__)

# Load the trained model (make sure to use the correct path)
model = joblib.load("C:\\PROJECT\\AutoCare IoT\\model.pkl")

# API endpoint to get anomaly predictions
@app.route('/predict_anomaly', methods=['POST'])
def predict_anomaly():
    data = request.json  # Get the data from the frontend

    # Convert the data into a DataFrame
    df = pd.DataFrame([data])

    # Remove columns that are not part of the model
    df = df.drop(columns=['timestamp', 'dtc'])

    # Make prediction using the trained model
    prediction = model.predict(df)
    
    # Return the result as JSON
    result = "Anomaly" if prediction[0] == -1 else "No anomaly"
    return jsonify({"prediction": result})

if __name__ == '__main__':
    app.run(debug=True)
