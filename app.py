import pandas as pd
from flask import Flask, jsonify, request, render_template
import joblib                               # TO unpack .gz
# import pickle                             # To use .pkl model
import json                               # To load in 'features.json'

# Load the model from 'berlin_model.pkl' file or 'berlin_model.gz'
# model = pickle.load(open('berlin_model.pkl', 'rb'))
model = joblib.load(open('berlin_model.gz', 'rb'))

# App
app = Flask(__name__)

# Could Remove this line of code: vvvv
# Setting this to True makes the returned JSON look not so jumbled up
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


# Routes
@app.route('/')
def index():
    return render_template('feature_input.html')


@app.route('/price', methods=['POST'])
def predict_price():
    # Takes data entered at index route via the 'feature_input.html' template
    data = dict(request.form)
    # Parse the file 'features.json' containing a skeleton JSON of feature
    # variables with default values set to '0'.  This block of code compares
    # the data from the request form to the default values from the JSON file
    # and makes changes depending on what the input was.  For features that
    # have multiple permutations (neighbourhood_group_cleansed, etc), whichever
    # was chosen in the drop-down list will be reassigned as an integer(1)
    # while the others remain an integer(0) which denotes that the listing is
    # not a particular feature permutation and thus, can be ran in the model.
    with open('features.json', 'r') as f:
        features_dict = json.load(f)
        for key, value in data.items():
            if key in features_dict:
                try:
                    features_dict[key] = float(value)
                except:
                    features_dict[key] = 0
            elif value in features_dict:
                features_dict[value] = 1
        # print(features_dict)
        data = features_dict

    # This code will take the variable 'data' and convert it from JSON into a
    # Pandas Dataframe which can be used with the next line of code
    df = pd.json_normalize(data)

    # Prediction based on the Dataframe containing feature values.
    # model.predict(df) returns the prediction as an n-dimensional array which
    # is not able to be 'jsonified' so you must grab the index at [0] to take
    # it out of the array and convert to JSON.  The prediction is rounded to
    # the nearest integer.
    results = int(model.predict(df)[0])

    # Return the features and predicted price as JSON
    # return jsonify(features=data, price=results)
    return jsonify(price=results)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
