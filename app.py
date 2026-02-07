@app.route("/admin")
def admin():
    if session.get("role")!="admin":
        return redirect("/")
    employees = Employee.query.all()
    return render_template("admin.html", employees=employees)
