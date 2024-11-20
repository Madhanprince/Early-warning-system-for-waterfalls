import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pygame

def play_sound():
    pygame.mixer.init()  # Initialize the mixer
    try:
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'static', 'alert_sound.mp3'))
        pygame.mixer.music.play(loops=0)  # Play once
    except pygame.error as e:
        print(f"Error playing sound: {e}")

def send_email(risk_level, details):
    from_address = 'madjeeve123@gmail.com'
    to_address = 'skamaleshwaran132@gmail.com'
    password = 'paub znrl cose eila'

    subject = f"Flood Risk Alert: {risk_level}"

    # HTML email body
    body = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flood Risk Alert</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body style="font-family: Arial, sans-serif; background-color: #f8f9fa; padding: 20px;">
    <div class="container">
        <div class="card">
            <div class="card-header text-white bg-primary">
                <h2>Flood Risk Alert: {risk_level}</h2>
            </div>
            <div class="card-body">
                <h4 class="card-title">Warning! The risk level of flooding is {risk_level}.</h4>
                <p class="card-text">
                    <strong>Details:</strong><br>
                    {details}
                </p>
                <h5 class="mt-4">Recommended Actions:</h5>
                <ul>
                    <li>Stay updated with weather alerts.</li>
                    <li>Evacuate the area if necessary.</li>
                    <li>Ensure your property is secured.</li>
                    <li>Keep emergency kits on hand.</li>
                </ul>
            </div>
            <div class="card-footer text-muted">
                <p>Stay safe and prepared!</p>
                <p>&copy; 2024 Waterfall Flood Risk Monitoring System</p>
            </div>
        </div>
    </div>
</body>
</html>
"""


    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_address, password)  
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == '__main__': 
    risk_level = "High Risk of Flood"
    details = "Water flow speed: 8.0 m/s, Water level: 12.5 meters. Immediate evacuation recommended."
    send_email(risk_level, details)
    play_sound()
    pygame.quit() #Quit pygame after use