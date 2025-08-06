from flask import Flask, request, jsonify,render_template
import pickle
import pandas as pd

app = Flask(__name__)

# Load the model once when the server starts (optional optimization)
with open("model.pkl", "rb") as f:
    model = pickle.load(f)



@app.route("/",methods=["GET"])
def home():
    return render_template("index.html")


def get_cleaned_data(form_data):
    
    gestation = float(form_data["gestation"])
    parity = int(form_data["parity"])
    age = float(form_data["age"])
    height = float(form_data["height"])
    weight = float(form_data["weight"])
    smoke = float(form_data["smoke"])

    cleaned_data={
        "gestation":[gestation],
        "parity":[parity],
        "age":[age],
        "height":[height],
        "weight":[weight],
        "smoke":[smoke]
    }

    return cleaned_data


@app.route("/prediction", methods=["POST"])
def get_prediction():
    try:
        # Get the JSON data from the request
        baby_data_form = request.form
        baby_data_form = get_cleaned_data(baby_data_form)

        # Convert JSON into DataFrame (wrap in list if it's a single row)
        df = pd.DataFrame(baby_data_form)

        # Make prediction
        prediction = model.predict(df)
        prediction = round(float(prediction),2)
        # Format prediction
        prediction_value = round(float(prediction), 2)

        # Return as JSON
        return render_template("index.html" , prediction=prediction)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)