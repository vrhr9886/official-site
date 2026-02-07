
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, session, jsonify,flash

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
from datetime import datetime, timedelta
from models import db, AdminProfile   
app = Flask(__name__)
app.secret_key = "super-secret-key"   # REQUIRED for session

# ---------------- CONFIG ----------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "admin.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "static/uploads")

db.init_app(app) 



with app.app_context():
    db.create_all()



# session lifetime = 1 minute (dashboard auto logout)
app.permanent_session_lifetime = timedelta(minutes=1)

# -----------------------------
# Email configuration
# -----------------------------
EMAIL = "kiranfuse9@gmail.com"
APP_PASSWORD = "dkkg mbht ucjf anrc"   # Gmail App Password

otp_store = {}  # {'email': {'otp': '123456', 'expiry': datetime}}
def send_otp(to_email, otp):
    msg = MIMEMultipart("alternative")
    msg['From'] = EMAIL
    msg['To'] = to_email
    msg['Subject'] = "Your OTP Code"

    # HTML BODY (Dark Theme + Green OTP Box)
#     html_body = f"""
# <!DOCTYPE html>
# <html>
# <head>
# <meta charset="UTF-8">
# <title>Admin Login OTP</title>
# </head>

# <body style="margin:0; padding:0; background:#0b1020; font-family:'Segoe UI', Arial, sans-serif;">

# <table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 0; background:#0b1020;">
# <tr>
# <td align="center">

# <!-- MAIN CONTAINER -->
# <table width="440" cellpadding="0" cellspacing="0"
#        style="background:#111827; border-radius:16px; overflow:hidden;
#               box-shadow:0 20px 60px rgba(0,0,0,0.7);">

# <!-- HEADER -->
# <tr>
# <td style="padding:26px; text-align:center;
#            background:linear-gradient(135deg,#0f766e,#22c55e);">
#     <h2 style="margin:0; color:#ffffff; font-size:22px; letter-spacing:0.6px;">
#         VRHR Soft Solutions
#     </h2>
#     <p style="margin:6px 0 0; color:#eafff8; font-size:13px;">
#         Admin Secure Login
#     </p>
# </td>
# </tr>

# <!-- BODY -->
# <tr>
# <td style="padding:34px; color:#e5e7eb;">

# <p style="font-size:16px; margin:0 0 12px;">
# Hello Admin,
# </p>

# <p style="font-size:14.5px; line-height:1.8; margin:0;">
# We received a request to access the <b>VRHR Soft Solutions Admin Dashboard</b>.
# Please use the OTP below to complete your secure login.
# </p>

# <!-- OTP CARD -->
# <div style="
#     margin:34px auto;
#     max-width:260px;
#     background:#020617;
#     border-radius:14px;
#     border:1px solid rgba(34,197,94,0.5);
#     padding:22px;
#     text-align:center;
#     box-shadow:inset 0 0 0 1px rgba(255,255,255,0.04),
#                0 0 30px rgba(34,197,94,0.25);
# ">
#     <div style="
#         font-size:40px;
#         font-weight:800;
#         color:#22c55e;
#         letter-spacing:12px;
#         font-family:Consolas, monospace;
#     ">
#         {otp}
#     </div>
# </div>

# <p style="font-size:13px; color:#9ca3af; line-height:1.7; margin:0;">
# ⏱ This OTP is valid for <b>30 seconds</b> only.<br>
# If you did not request this login, please ignore this email or contact system security immediately.
# </p>

# </td>
# </tr>

# <!-- FOOTER -->
# <tr>
# <td style="background:#020617; padding:18px; text-align:center;">
#     <p style="margin:0; color:#6b7280; font-size:12px; line-height:1.6;">
#         © 2026 VRHR Soft Solutions Pvt. Ltd.<br>
#         Secure Admin Authentication System
#     </p>
# </td>
# </tr>

# </table>
# <!-- END CONTAINER -->

# </td>
# </tr>
# </table>

# </body>
# </html>
# """

    html_body = f"""
   <!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Admin Login OTP</title>
</head>

<body style="margin:0; padding:0; background:#0b0f14; font-family:Segoe UI, Arial, sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0" style="padding:30px; background:#0b0f14;">
<tr>
<td align="center">

<!-- MAIN CARD -->
<table width="420" cellpadding="0" cellspacing="0"
       style="background:#121826; border-radius:14px; overflow:hidden; box-shadow:0 0 25px rgba(0,0,0,0.6);">

<!-- HEADER -->
<tr>
<td style="background:linear-gradient(135deg,#1abc9c,#16a085);
           padding:20px; text-align:center;">
    <h2 style="margin:0; color:#ffffff; letter-spacing:0.5px;">
        VRHR Soft Solutions
    </h2>
    <p style="margin:5px 0 0; color:#eafff8; font-size:13px;">
        Admin Secure Login
    </p>
</td>
</tr>

<!-- CONTENT -->
<tr>
<td style="padding:30px; color:#e6e9ef;">

<p style="font-size:16px; margin-top:0;">Hello Admin,</p>

<p style="font-size:14.5px; line-height:1.7;">
We received a request to access the <b>VRHR Soft Solutions Admin Dashboard</b>.
Please use the OTP below to complete your secure login.
</p>

<!-- OTP BOX -->
<div style="
    margin:28px auto;
    width:220px;
    text-align:center;
    background:#0f172a;
    border:2px solid #1abc9c;
    border-radius:12px;
    padding:18px;
    font-size:38px;
    font-weight:700;
    color:#1abc9c;
    letter-spacing:10px;
    box-shadow:0 0 12px rgba(26,188,156,0.35);
">
    { otp }
</div>

<p style="font-size:13px; color:#9aa4b2; line-height:1.6;">
⏱ This OTP is valid for <b>30 seconds</b> only.<br>
If you did not request this login, please ignore this email or contact system security immediately.
</p>

</td>
</tr>

<!-- FOOTER -->
<tr>
<td style="background:#0f172a; padding:14px; text-align:center;">
    <p style="margin:0; color:#8b95a7; font-size:12px;">
        © 2026 VRHR Soft Solutions Pvt. Ltd.<br>
        Secure Admin Authentication System
    </p>
</td>
</tr>

</table>
<!-- END CARD -->

</td>
</tr>
</table>

</body>
</html>
"""
    msg.attach(MIMEText(html_body, "html"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, APP_PASSWORD)
    server.send_message(msg)
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
    return render_template("index.html")

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
# ----------------------------------------
@app.route("/salary")
def salary():
    if "user" not in session:
        return redirect(url_for("login"))
    # Ensure salarysleep.html is inside the 'templates' folder
    return render_template("salarysleep.html")

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
    session.clear() # Session poori tarah saaf
    flash("You have been logged out successfully!", "info") 
    return redirect(url_for("home")) # 'home' route pe bhej raha hai

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user" not in session:
        return redirect(url_for("login"))

    profile = AdminProfile.query.first()

    if request.method == "POST":
        if not profile:
            profile = AdminProfile()
            db.session.add(profile)

        profile.name = request.form.get("name")
        profile.email = request.form.get("email")
        profile.role = request.form.get("role")
        profile.phone = request.form.get("phone")
        profile.address = request.form.get("address")

        image = request.files.get("image")
        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            profile.image = filename

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile"))

    return render_template("adminprofile.html", profile=profile)
    if "user" not in session:
        return redirect(url_for("login"))

    profile = AdminProfile.query.first()

    if request.method == "POST":
        if not profile:
            profile = AdminProfile()
            db.session.add(profile) # Naya profile hai toh add karein

        # Data update karein
        profile.name = request.form.get("name")
        profile.email = request.form.get("email")
        profile.role = request.form.get("role")
        profile.phone = request.form.get("phone")
        profile.address = request.form.get("address")

        # Image handling
        image = request.files.get("image")
        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            profile.image = filename

        db.session.commit() # Save to SQLite
        return redirect(url_for("profile"))

    return render_template("adminprofile.html", profile=profile)

    if "user" not in session:
        return redirect(url_for("login"))

    profile = AdminProfile.query.first()

    # ✅ DEMO DATA (only when DB empty)
    demo_profile = {
        "name": "Demo Admin",
        "email": "admin@company.com",
        "role": "Administrator",
        "phone": "9999999999",
        "address": "Company Head Office, India",
        "image": "default.png"
    }

    if request.method == "POST":
        if not profile:
            profile = AdminProfile()

        profile.name = request.form.get("name")
        profile.email = request.form.get("email")
        profile.role = request.form.get("role")
        profile.phone = request.form.get("phone")
        profile.address = request.form.get("address")

        image = request.files.get("image")
        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            profile.image = filename

        db.session.add(profile)
        db.session.commit()

        return redirect(url_for("profile"))

    return render_template(
        "adminprofile.html",
        profile=profile,
        demo=demo_profile
    )


    if "user" not in session:
        return redirect(url_for("login"))

    profile = AdminProfile.query.first()

    if request.method == "POST":

        if not profile:
            profile = AdminProfile()

        profile.name = request.form.get("name")
        profile.email = request.form.get("email")
        profile.role = request.form.get("role")
        profile.phone = request.form.get("phone")
        profile.address = request.form.get("address")

        image = request.files.get("image")
        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            profile.image = filename

        db.session.add(profile)
        db.session.commit()

        return redirect(url_for("profile"))  # ✅ reload with saved data

    return render_template("adminprofile.html", profile=profile)

if __name__ == "__main__":
    app.run(debug=True)
