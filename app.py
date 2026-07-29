from flask import Flask, render_template, request, redirect, session, flash, send_file
import sqlite3
import pandas as pd
import joblib

from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = "smartlender123"

model = joblib.load("model.pkl")
# ---------------- DATABASE ---------------- #

def init_db():

    conn = sqlite3.connect("users.db")

    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()

    conn.close()

init_db()
# ---------------- HOME ---------------- #

@app.route("/")
def home():
    return render_template("index.html")
# ---------------- REGISTER ---------------- #

# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE email=?", (email,))
        user = c.fetchone()

        conn.close()

        if user and check_password_hash(user[3], password):
            session["user"] = user[1]
            return redirect("/dashboard")

        flash("Invalid Email or Password")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        try:
            c.execute(
                "INSERT INTO users(name,email,password) VALUES(?,?,?)",
                (name, email, password)
            )
            conn.commit()
            flash("Registration Successful!")
            return redirect("/login")

        except sqlite3.IntegrityError:
            flash("Email already exists.")

        finally:
            conn.close()

    return render_template("register.html")


# ---------------- DASHBOARD ---------------- #

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        user=session["user"]
    )


# ---------------- PROFILE ---------------- #

@app.route("/profile")
def profile():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "profile.html",
        user=session["user"],
        email="aslam@gmail.com"
    )


# ---------------- APPLY LOAN ---------------- #

@app.route("/apply")
def apply():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "apply_loan.html",
        user=session["user"]
    )


# ---------------- PREDICT ---------------- #
@app.route("/predict", methods=["POST"])
def predict():

    if "user" not in session:
        return redirect("/login")

    gender = 1 if request.form["Gender"] == "Male" else 0
    married = 1 if request.form["Married"] == "Yes" else 0

    dep = request.form["Dependents"]
    if dep == "3+":
        dependents = 3
    elif dep.isdigit():
        dependents = int(dep)
    else:
        dependents = 0

    education = 1 if request.form["Education"] == "Graduate" else 0
    self_employed = 1 if request.form["Self_Employed"] == "Yes" else 0

    applicant_income = float(request.form["ApplicantIncome"])
    coapplicant_income = float(request.form["CoapplicantIncome"])
    loan_amount = float(request.form["LoanAmount"])
    loan_term = float(request.form["Loan_Amount_Term"])
    credit_history = float(request.form["Credit_History"])

    area = request.form["Property_Area"]
    if area == "Urban":
        property_area = 2
    elif area == "Semiurban":
        property_area = 1
    else:
        property_area = 0

    data = [[
        gender,
        married,
        dependents,
        education,
        self_employed,
        applicant_income,
        coapplicant_income,
        loan_amount,
        loan_term,
        credit_history,
        property_area
    ]]

    prediction = model.predict(data)

    if prediction[0] == 1:
        result = "✅ Loan Approved"
    else:
        result = "❌ Loan Rejected"

    

    return render_template(
        "result.html",
        result=result,
        user=session["user"]
    )

# ---------------- LOAN HISTORY ---------------- #

@app.route("/loan-history")
def loan_history():

    if "user" not in session:
        return redirect("/login")

    loans = [
        {
            "id": 1,
            "name": session["user"],
            "amount": 250000,
            "status": "Approved",
            "date": "08-07-2026"
        }
    ]

    return render_template(
        "loan_history.html",
        loans=loans
    )




# ---------------- FORGOT PASSWORD ---------------- #

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":
        flash("Password reset feature will be available soon.")
        return redirect("/login")

    return render_template("forgot_password.html")
# ---------------- ADMIN DASHBOARD ---------------- #

@app.route("/admin")
def admin():

    if "user" not in session:
        return redirect("/login")

    return render_template("admin_dashboard.html")


# ---------------- PDF REPORT ---------------- #

@app.route("/download-report")
def download_report():

    if "user" not in session:
        return redirect("/login")

    filename = "Loan_Report.pdf"

    c = canvas.Canvas(filename)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(170, 800, "Smart Lender AI")

    c.setFont("Helvetica", 14)
    c.drawString(50, 750, f"Applicant : {session['user']}")
    c.drawString(50, 720, "Loan Prediction Report")
    c.drawString(50, 690, "Status : Generated Successfully")

    c.save()

    return send_file(filename, as_attachment=True)
# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.")

    return redirect("/login")


# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    app.run(debug=True)




    