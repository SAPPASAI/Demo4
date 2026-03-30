from flask import render_template, Flask, request, redirect, url_for, session
import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

knn = joblib.load('Models/knn_model.pkl')
scaler = joblib.load('Models/scaler.pkl')

USERS = {
    'user1': 'pass1',
    'user2': 'pass2',
    'user3': 'pass3'
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect(url_for('welcome'))

    return render_template('login.html')

@app.route('/home')
def welcome():
    if 'username' in session:
        return render_template('Home.html')

    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('login'))

    features = [
        int(request.form['Clump']),
        int(request.form['UnifSize']),
        int(request.form['UnifShape']),
        int(request.form['MargAdh']),
        int(request.form['SingEpiSize']),
        int(request.form['BareNuc']),
        int(request.form['BlandChrom']),
        int(request.form['NormNucl']),
        int(request.form['Mit'])
    ]
    
        # Scale input
    features = scaler.transform([features])

    prediction = knn.predict(features)

    if prediction[0] == 2:
        result = "Benign"
    else:
        result = "Malignant"

    return render_template('Home.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)