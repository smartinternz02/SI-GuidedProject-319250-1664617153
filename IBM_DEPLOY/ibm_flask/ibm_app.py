
# importing the necessary dependencies
import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import pickle
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "0cJ7n0wwaMHrRtGePMMIDfpkmYg7ue8E-NwwyDj9Dxmo"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__) # initializing a flask app


@app.route('/')# route to display the home page
def home():
    return render_template('home.html') #rendering the home page

@app.route('/Prediction',methods=['POST','GET'])
def prediction():
    return render_template('index.html')

@app.route('/Home',methods=['POST','GET'])
def my_home():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])# route to show the predictions in a web UI
def predict():
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    #  reading the inputs given by the user
    age=request.form['age']
    blood_urea= request.form["blood_urea"]
    blood_glucose_random= request.form["blood_glucose_random"]
    anemia = request.form["anemia"]
    coronary_artery_disease = request.form["coronary_artery_disease"]
    pus_cell = request.form["pus_cell"]
    red_blood_cells = request.form["red_blood_cell"]
    diabetesmellitus = request.form["diabetesmellitus"]
    pedal_edema = request.form["pedal_edema"]
    
    
    t = [[int(age),int(blood_urea),int(blood_glucose_random),int(anemia),int(coronary_artery_disease),int(pus_cell),
          int(red_blood_cells),int(diabetesmellitus),int(pedal_edema)]]
    
    payload_scoring = {"input_data": [{"field": [['age','blood_urea', 'blood_glucose_random', 'anemia', 'coronary_artery_disease', 'pus_cell', 'red_blood_cells',
       'diabetesmellitus', 'pedal_edema']], "values": t}]}
    
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/92cfa809-70eb-44c6-b51a-cddcad0bfbe0/predictions?version=2022-10-13', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    pred = predictions[predictions][0]['values'][0][0]
    print("Final prediction :",pred)
    if (pred == 0):
       print("you have kidney disease")
    else:
       print("you don't have any kidney disease")
    #reading the inputs given by the user
    input_features = [float(x) for x in request.form.values()]
    features_value = [np.array(input_features)]
    
    features_name = ['age','blood_urea', 'blood_glucose_random', 'anemia',
      'coronary_artery_disease', 'pus_cell', 'red_blood_cells',
      'diabetesmellitus', 'pedal_edema']
    
    df = pd.DataFrame(features_value, columns=features_name)
    
     #predictions using the loaded model file
    output = model.predict(df)
    
    # showing the prediction results in a UI# showing the prediction results in a UI
    return render_template('result.html', prediction_text=pred)

if __name__ == '__main__':
    # running the app
    app.run(debug=True)
