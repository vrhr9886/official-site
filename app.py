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
    <html>
    <head>
    <title>VRHR Login</title>
    <style>
    body{font-family:Arial;background:#0b5ed7;display:flex;justify-content:center;align-items:center;height:100vh}
    .box{background:white;padding:40px;border-radius:10px;width:300px;text-align:center}
    input{width:90%;padding:10px;margin:10px}
    button{background:#0b5ed7;color:white;border:none;padding:10px 20px;border-radius:6px}
    </style>
    </head>
    <body>
    <div class='box'>
    <h2>VRHR Soft Solutions</h2>
    <form method='post'>
    <input name='username' placeholder='Username'><br>
    <input name='password' type='password' placeholder='Password'><br>
    <button>Login</button>
    </form>
    </div>
    </body>
    </html>
    """
