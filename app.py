import os
from flask import Flask, flash, render_template, request, redirect, url_for, session
import pandas as pd
import joblib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils import send_email, play_sound

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'

model = joblib.load('model.pkl')

USERNAME = 'admin'
PASSWORD = 'admin'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    waterfall_data = [
        {'date': '2024-11-01', 'time': '08:00', 'temperature': 25, 'humidity': 80, 'water_flow_speed': 1.2, 'water_level': 3.4},
        {'date': '2024-11-01', 'time': '09:00', 'temperature': 24, 'humidity': 82, 'water_flow_speed': 1.3, 'water_level': 3.5},
        {'date': '2024-11-01', 'time': '10:00', 'temperature': 23, 'humidity': 85, 'water_flow_speed': 1.5, 'water_level': 3.7},
    ]

    risk_level = None
    details = None
    if 'risk_level' in session:
        risk_level = session['risk_level']
        details = session['details']

    return render_template('dashboard.html', waterfall_data=waterfall_data, risk_level=risk_level, details=details)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            file = request.files['csv_file']
            if file and file.filename.endswith('.csv'):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)

                df = pd.read_csv(filepath)

                prediction = predict_risk(df)

                session['risk_level'] = prediction['risk']
                session['details'] = prediction['details']

                if prediction['risk'] == "High Risk of Flood":
                    send_email(prediction['risk'], prediction['details'])
                    play_sound()

                return redirect(url_for('dashboard'))
            else:
                flash("Please upload a CSV file.", "danger")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")
            return render_template('predict.html')

    return render_template('predict.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash('Invalid login credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

def predict_risk(df):
    features = df[['Temperature', 'Humidity', 'Water Flow Speed', 'Water Level']]

    predictions = model.predict(features)

    result = {
        'risk': predictions[0],
        'details': f"Prediction result based on the water level: {df['Water Level'].max()} meters, and water flow speed: {df['Water Flow Speed'].max()} m/s."
    }

    return result

if __name__ == '__main__':
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        if not os.path.exists("uploads"):
            os.makedirs("uploads")


    app.run(debug=True)