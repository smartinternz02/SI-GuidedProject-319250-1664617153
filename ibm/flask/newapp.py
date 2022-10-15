import requests
import json
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "0cJ7n0wwaMHrRtGePMMIDfpkmYg7ue8E-NwwyDj9Dxmo"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"field": [["age","blood_urea","blood glucose random","anemia","coronary_artery_disease","pus_cell","red_blood_cells","diabetesemellitus","pedal_edema"]], "values": [50,17.0,102.000000,0,0,1,1,1,0]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/92cfa809-70eb-44c6-b51a-cddcad0bfbe0/predictions?version=2022-10-13', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
predictions = response_scoring.json()
pred = predictions['predictions'][0]['values'][0][0]
if (pred == 0):
    print("you have kidney disease")
else:
    print("you don't have any kidney disease")