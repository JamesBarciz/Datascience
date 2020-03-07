## AirBnB Application

For this project, our goal is to accurately predict the price of a potential listing for AirBnB in the city of Berlin, Germany.

**DS Unit3 Portion** [*Heroku Application*](https://airbnb-berlin-price-predict.herokuapp.com/).

## Data Science Unit 3

Our main objectives as part of dspt3-Unit_3 were to:

1. Obtain a dataset pertinent to Berlin AirBnB listings and extract important features needed to make the app as accurate as possible both in genuineness and predictiveness.

2. Relay said features to the Back End web developer to help create the schema to be used for the database they will build using PostgreSQL.

3. Make predictions accessible to the team by deploying a Flask API to receive inputs and output predicted optimal price in JSON format.

## Notebook

---[*My personal notebook*](https://github.com/JamesBarciz/Datascience/blob/master/airbnb_revised_Mar_2.ipynb) used for most of the Build Week---

The [final model notebook](https://github.com/JamesBarciz/Datascience/blob/master/airbnb_notebook.ipynb) (90% created and worked on by Ahmed Hadzisulejmanovic) for this repo focuses on cleaning and tidying up the dataset 'listings_summary.csv' - [raw data](https://raw.githubusercontent.com/JamesBarciz/Datascience/master/listings_summary.csv) - which is one of many CSVs contained in a zip file downloaded from this [Kaggle Webpage](https://www.kaggle.com/brittabettendorf/berlin-airbnb-data).  Much of the code was not going to be useful as there are 96 features total, most of which have high cardinality or more than 80% NaN values and thus, were removed.  Columnal values that included a dollar sign had to be dealt with appropriately by stripping the sign **$** anc converting from a string to an integer or float.  The target column 'price' had a very wide range despite 75% of the data being around $70 or less so before testing the data, a subset was taken where the 'price' column contained only values less than a value of 400 (dollars).

## Model

The final model we decided on used [OneHotEncoding](https://contrib.scikit-learn.org/categorical-encoding/onehot.html) of the categorical features of which, there were six ('neighbourhood_group_cleansed', 'property_type', 'room_type', 'bed_type', 'instant_bookable', and 'cancellation_policy') and, addition, six continuous features (as floats: 'accommodates', 'bedrooms', 'cleaning_fee', 'extra_people', 'guests_included', and 'minimum_nights').  To combat the NaN values left, [SimpleImputer](https://scikit-learn.org/stable/modules/generated/sklearn.impute.SimpleImputer.html) was used (strategy='mean').  The best accuracy we could come up with was from [RandomForestRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html) which then, was worked on further using [RandomizedSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.RandomizedSearchCV.html) resulting in the hyperparameters: max_depth=15, max_features=0.452.., n_estimators=387 - obtaining a mean-absolute-error of $12 on the training data and $17 on the test data.  My hypothesis for this wide range is because some of the categorical values had minimal presence within the dataset therefore, creating a bad distribution of the data.  Nevertheless, the file was too large to upload as a .pkl file so, it had to be compressed using [Joblib](https://joblib.readthedocs.io/en/latest/) into a .gz file of about 25MB.

The process of choosing these features stemmed not only from wanting to obtain a good accuracy but, because they were possible features that a user, who would be listing their property, might include above all else.

## App

[*python script*](https://github.com/JamesBarciz/Datascience/blob/master/app.py)

The app model, used to give Back End and Front End a start for API access, uses [Flask](https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/) and contains two routes: '/' (index) and '/price' (prediction page).  A 'POST' request method is added to both the predicted price route as well as the [HTML template](https://github.com/JamesBarciz/Datascience/blob/master/templates/feature_input.html) used to input values for the features.  Within the template, numeric inputs (with a default of 0) were added for the six continuous features and drop-downs were added for the remaining six categorical features.

In order for this application to work (make a prediction using *all* of the features and their permutations), a [*JSON file*](https://github.com/JamesBarciz/Datascience/blob/master/features.json) had to be created which set every feature to a default of 0.  Within the '/price' route, the code in lines 37-48 will check the values obtained by the post request against the values within the JSON file.  Should any of the keys called by the input match the key in the JSON file skeleton for the continuous features, the loop will *try* to convert the value into a float and replace the defaults within the skeleton else, leave it 0 - this is because not entering a number (or anything) in the input will cause the app to crash in trying to convert a string into a float.  For the categorical features, the value of 0 will be replaced by a 1 (*true*) for whichever input is chosen using the drop-down list, leaving the others as 0 (*false*).

Afterwards, the updated values are converted from JSON to a Pandas dataframe so that it may be used with the regression model.  The obtained result is in the format of an n-dimensional array ('ndarray([])') so, we must index the 0th value and pass that through [jsonify](https://flask.palletsprojects.com/en/1.1.x/api/#flask.json.jsonify) in the format of "price"=predicted_price.

Clicking the 'Submit' button will take you to the '/price' route and display the following as {"key": value}:
1. "features": dictionary of inputted feature values
2. "price": predicted price