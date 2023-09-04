from flask import Flask,request,render_template
#import pickle
import pandas as pd
import requests
app=Flask(__name__)
#model=pickle.load(open('classification_model.pkl','rb'))
@app.route('/')
def home():
    return render_template('input.html')

@app.route('/input', methods = ['POST'] )
def pred():
    input = pd.DataFrame({
    'Gender':[float(request.form.get('Gender'))],
    'Age' : [float(request.form.get('Age'))],
    'CGPA'  : [float(request.form.get('CGPA'))],
    'Internships'  : [float(request.form.get('Internships'))],
    'HistoryOfBacklogs'  : [float(request.form.get('HistoryOfBacklogs'))],
    'Stream'  : [float(request.form.get('Stream'))],
    "Hostel" : [float(request.form.get('Hostel'))]
    })

    # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
    API_KEY = "g8Z5oDQDISrVy9Tvr-U-fTUWs0XZEYfawawjrL-sGjdu"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
    API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": ["Age",
                                "Internships",
                                "CGPA",
                                "Hostel",
                                "HistoryOfBacklogs",
                                "StreamLabelEncoder",
                                "GenderLabelEncoder"], 
                                       "values": [[input["Age"][0],input["Internships"][0],
                                                   input["CGPA"][0],input["Hostel"][0],input["HistoryOfBacklogs"][0],
                                                   input["Stream"][0],input["Gender"][0]]]}]}

    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/cf78a8a6-4eb1-4d55-866b-5eb925d14327/predictions?version=2021-05-01', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    op = response_scoring.json()["predictions"][0]["values"][0][0]
    if op==1:
        op="You are eligible for placement"
    else:
        op="You are not eligible for placement."
    #print(op)
    return render_template('input.html',Output=str(op))

if __name__ == '_main_':
    app.run()