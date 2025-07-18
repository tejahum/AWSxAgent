from flask import Flask, request, jsonify, session
import random
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session

# Replace with your email and app password
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"

# Generate and send OTP
def send_otp(email, otp):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your Login Code"
    message["From"] = EMAIL_ADDRESS
    message["To"] = email

    html = f"<html><body><p>Your login code is: <strong>{otp}</strong></p></body></html>"
    message.attach(MIMEText(html, "html"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, email, message.as_string())

@app.route("/send-code", methods=["POST"])
def send_code():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email required"}), 400

    otp = random.randint(100000, 999999)
    session["otp"] = str(otp)
    session["email"] = email

    send_otp(email, otp)
    return jsonify({"message": "OTP sent"}), 200

@app.route("/verify-code", methods=["POST"])
def verify_code():
    data = request.get_json()
    code = data.get("code")
    if session.get("otp") == code:
        return jsonify({"message": "Verified ✅"}), 200
    else:
        return jsonify({"error": "Invalid code ❌"}), 400

if __name__ == "__main__":
    app.run(debug=True)
