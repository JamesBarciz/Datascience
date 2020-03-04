import pandas as pd
from flask import Flask, jsonify, request
import pickle

# Load the model from berlin_model.pkl file
model = pickle.load(open('berlin_model.pkl', 'rb'))

# App
app = Flask(__name__)

# Routes
@app.route('/', methods=['POST'])
def Optimal_Price():
    return "Get Optimal Price"

def predict_price():
    # Takes data entered via post request
    feature_data = request.get_json(force=True)

    # Convert the data into a dataframe
    feature_data.update((x, [y]) for x, y in feature_data.items())
    df = pd.DataFrame.from_dict(feature_data)

    # Prediction based on the feature values
    result = model.predict(df)

    # Output which is sent to browser
    output = {'results': int(result[0])}

    # Return the predicted value as JSON
    return jsonify(results=output)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
