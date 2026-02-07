from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "vrhr_secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# ---------- DATABASE ----------
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    role = db.Column(db.String(20))

with app.app_context():
    db.create_all()
    if not Employee.query.filter_by(username="vrhrsoftsolutions").first():
        admin = Employee(name="Admin", username="vrhrsoftsolutions", password="Vrhr@9886", role="admin")
        e1 = Employee(name="HR Shubham Vishwakarma", username="shubham", password="1234", role="employee")
        e2 = Employee(name="Kiran Bari", username="kiran", password="1234", role="employee")
        e3 = Employee(name="Gaurav Rathod", username="gaurav", password="1234", role="employee")
        e4 = Employee(name="Swapnil Nagpure", username="swapnil", password="1234", role="employee")
        db.session.add_all([admin,e1,e2,e3,e4])
        db.session.commit()

# ---------- LOGIN ----------
@app.route("/", methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=request.form.get("username")
        p=request.form.get("password")
        user=Employee.query.filter_by(username=u,password=p).first()
        if user:
            session["user"]=user.username
            session["role"]=user.role
            if user.role=="admin":
                return redirect("/admin")
            else:
                return redirect("/employee")

    return """
    <h2>VRHR Soft Solutions Login</h2>
    <form method='post'>
    Username:<br><input name='username'><br>
    Password:<br><input name='password' type='password'><br><br>
    <button>Login</button>
    </form>
    """

# ---------- ADMIN ----------
@app.route("/admin")
def admin():
    if session.get("role")!="admin":
        return redirect("/")
    employees = Employee.query.all()
    return "<h2>Admin Panel</h2>Software starting...<br><a href='/logout'>Logout</a>"

# ---------- EMPLOYEE ----------
@app.route("/employee")
def employee():
    if "user" not in session:
        return redirect("/")
    return "<h2>Employee Dashboard</h2><a href='/logout'>Logout</a>"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run()
