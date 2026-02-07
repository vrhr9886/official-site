from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "super-secret-key"   # REQUIRED for session

# session lifetime = 1 minute (dashboard auto logout)
app.permanent_session_lifetime = timedelta(minutes=1)

# -----------------------------
# Email configuration
# -----------------------------
EMAIL = "kiranfuse9@gmail.com"
APP_PASSWORD = "dkkg mbht ucjf anrc"   # Gmail App Password

otp_store = {}  # {'email': {'otp': '123456', 'expiry': datetime}}

def send_otp(to_email, otp):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = to_email
    msg['Subject'] = "Your OTP Code"

    body = f"Your OTP is {otp}. It will expire in 1 minute."
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL, APP_PASSWORD)
    server.sendmail(EMAIL, to_email, msg.as_string())
    server.quit()

    print("OTP sent to", to_email)

# -----------------------------

# resend otp
@app.route("/resend-otp", methods=["POST"])
def resend_otp():
    otp = random.randint(100000, 999999)

    otp_store["kiranfuse52@gmail.com"] = {
        "otp": str(otp),
        "expiry": datetime.now() + timedelta(minutes=1)
    }

    send_otp("kiranfuse52@gmail.com", otp)
    return jsonify({"status": "otp_sent"})

# Routes
# -----------------------------
@app.route("/")
def home():
    return redirect(url_for("login"))

# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if username == "admin" and password == "admin":
        otp = random.randint(100000, 999999)

        otp_store["kiranfuse52@gmail.com"] = {
            "otp": str(otp),
            "expiry": datetime.now() + timedelta(minutes=1)   # ✅ OTP 1 minute
        }

        send_otp("kiranfuse52@gmail.com", otp)
        return jsonify({"status": "otp_sent"})

    return jsonify({"status": "invalid"})

# -----------------------------
@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    otp_input = request.form.get("otp")
    record = otp_store.get("kiranfuse52@gmail.com")

    if not record:
        return jsonify({"status": "invalid"})

    if datetime.now() > record["expiry"]:
        otp_store.pop("kiranfuse52@gmail.com", None)
        return jsonify({"status": "expired"})

    if otp_input == record["otp"]:
        session.permanent = True     # ✅ start session
        session["user"] = "admin"
        otp_store.pop("kiranfuse52@gmail.com", None)
        return jsonify({"status": "success"})

    return jsonify({"status": "invalid"})

# -----------------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")

# -----------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
