import pandas as pd
from flask import Flask, jsonify, request
import pickle

# Load the model from model.pkl file
model = pickle.load(open('berlin_model.pkl', 'rb'))

# App
app = Flask(__name__)

# Routes
@app.route('/', methods=['POST'])

def predict():
    # Get the data
    data = request.get_json(force=True)

    # Convert the data into a dataframe
    data.update((x, [y]) for x, y in data.items())
    data_df = pd.DataFrame.from_dict(data)

    # Predictions
    result = model.predict(data_df)

    # Output which is sent to browser
    output = {'results': int(result[0])}

    # Return the data as JSON
    return jsonify(results=output)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
