from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()   # ✅ MUST be here (TOP LEVEL)

class AdminProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    role = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    image = db.Column(db.String(200))
