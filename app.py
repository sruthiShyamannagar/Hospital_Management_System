from flask import Flask, render_template, request, redirect
import mysql.connector
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv(override=True)

# MySQL connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM patients")
    patient_count = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM doctors")
    doctor_count = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM appointments")
    appointment_count = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM departments")
    department_count = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM billing")
    bill_count = cursor.fetchone()["total"]

    cursor.close()

    return render_template(
        "dashboard.html",
        patient_count=patient_count,
        doctor_count=doctor_count,
        appointment_count=appointment_count,
        department_count=department_count,
        bill_count=bill_count
    )

@app.route("/patients/add", methods=["GET", "POST"])
def add_patient():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        address = request.form["address"]
        disease = request.form["disease"]

        cursor = db.cursor()

        query = """
        INSERT INTO patients
        (name, age, gender, phone, address, disease)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            name,
            age,
            gender,
            phone,
            address,
            disease
        )

        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return redirect("/patients")

    return render_template("patients/add.html")

@app.route("/patients")
def patients():
    db.ping(reconnect=True, attempts=3, delay=2)
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM patients ORDER BY patient_id DESC")
    patients = cursor.fetchall()

    cursor.close()

    return render_template("patients/list.html", patients=patients)

@app.route("/patients/edit/<int:patient_id>", methods=["GET", "POST"])
def edit_patient(patient_id):

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        address = request.form["address"]
        disease = request.form["disease"]

        query = """
        UPDATE patients
        SET name=%s, age=%s, gender=%s, phone=%s,
            address=%s, disease=%s
        WHERE patient_id=%s
        """

        values = (
            name, age, gender, phone,
            address, disease, patient_id
        )

        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return redirect("/patients")

    cursor.execute(
        "SELECT * FROM patients WHERE patient_id=%s",
        (patient_id,)
    )

    patient = cursor.fetchone()
    cursor.close()

    return render_template("patients/edit.html", patient=patient)

@app.route("/patients/delete/<int:patient_id>")
def delete_patient(patient_id):

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE patient_id=%s",
        (patient_id,)
    )

    db.commit()
    cursor.close()

    return redirect("/patients")

@app.route("/doctors/add", methods=["GET", "POST"])
def add_doctor():

    if request.method == "POST":

        name = request.form["name"]
        specialization = request.form["specialization"]
        phone = request.form["phone"]
        email = request.form["email"]
        experience = request.form["experience"]

        cursor = db.cursor()

        query = """
        INSERT INTO doctors
        (name, specialization, phone, email, experience)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            name,
            specialization,
            phone,
            email,
            experience
        )

        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return redirect("/doctors/add")

    return render_template("doctors/add.html")

@app.route("/doctors")
def doctors():

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM doctors ORDER BY doctor_id DESC")
    doctors = cursor.fetchall()

    cursor.close()

    return render_template("doctors/list.html", doctors=doctors)

@app.route("/doctors/edit/<int:doctor_id>", methods=["GET", "POST"])
def edit_doctor(doctor_id):

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        name = request.form["name"]
        specialization = request.form["specialization"]
        phone = request.form["phone"]
        email = request.form["email"]
        experience = request.form["experience"]

        query = """
        UPDATE doctors
        SET name=%s,
            specialization=%s,
            phone=%s,
            email=%s,
            experience=%s
        WHERE doctor_id=%s
        """

        values = (
            name,
            specialization,
            phone,
            email,
            experience,
            doctor_id
        )

        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return redirect("/doctors")

    cursor.execute(
        "SELECT * FROM doctors WHERE doctor_id=%s",
        (doctor_id,)
    )

    doctor = cursor.fetchone()
    cursor.close()

    return render_template("doctors/edit.html", doctor=doctor)


@app.route("/doctors/delete/<int:doctor_id>")
def delete_doctor(doctor_id):

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM doctors WHERE doctor_id=%s",
        (doctor_id,)
    )

    db.commit()
    cursor.close()

    return redirect("/doctors")

@app.route("/appointments/add", methods=["GET", "POST"])
def add_appointment():

    if request.method == "POST":

        patient_id = request.form["patient_id"]
        doctor_id = request.form["doctor_id"]
        appointment_date = request.form["appointment_date"]
        appointment_time = request.form["appointment_time"]
        reason = request.form["reason"]

        cursor = db.cursor()

        query = """
        INSERT INTO appointments
        (patient_id, doctor_id, appointment_date, appointment_time, reason)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            patient_id,
            doctor_id,
            appointment_date,
            appointment_time,
            reason
        )

        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return redirect("/appointments/add")

    return render_template("appointments/add.html")

@app.route("/appointments")
def appointments():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM appointments
        ORDER BY appointment_id DESC
    """)

    appointments = cursor.fetchall()

    cursor.close()

    return render_template(
        "appointments/list.html",
        appointments=appointments
    )

@app.route("/appointments/edit/<int:appointment_id>", methods=["GET", "POST"])
def edit_appointment(appointment_id):

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        patient_id = request.form["patient_id"]
        doctor_id = request.form["doctor_id"]
        appointment_date = request.form["appointment_date"]
        appointment_time = request.form["appointment_time"]
        reason = request.form["reason"]
        status = request.form["status"]

        query = """
        UPDATE appointments
        SET patient_id=%s,
            doctor_id=%s,
            appointment_date=%s,
            appointment_time=%s,
            reason=%s,
            status=%s
        WHERE appointment_id=%s
        """

        values = (
            patient_id,
            doctor_id,
            appointment_date,
            appointment_time,
            reason,
            status,
            appointment_id
        )

        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return redirect("/appointments")

    cursor.execute(
        "SELECT * FROM appointments WHERE appointment_id=%s",
        (appointment_id,)
    )

    appointment = cursor.fetchone()
    cursor.close()

    return render_template(
        "appointments/edit.html",
        appointment=appointment
    )


@app.route("/appointments/delete/<int:appointment_id>")
def delete_appointment(appointment_id):

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM appointments WHERE appointment_id=%s",
        (appointment_id,)
    )

    db.commit()
    cursor.close()

    return redirect("/appointments")

@app.route("/departments/add", methods=["GET", "POST"])
def add_department():

    if request.method == "POST":

        department_name = request.form["department_name"]
        description = request.form["description"]

        cursor = db.cursor()

        query = """
        INSERT INTO departments
        (department_name, description)
        VALUES (%s, %s)
        """

        values = (department_name, description)

        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return redirect("/departments/add")

    return render_template("departments/add.html")

@app.route("/departments")
def departments():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM departments
        ORDER BY department_id DESC
    """)

    departments = cursor.fetchall()

    cursor.close()

    return render_template(
        "departments/list.html",
        departments=departments
    )

@app.route("/departments/edit/<int:department_id>", methods=["GET", "POST"])
def edit_department(department_id):

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        department_name = request.form["department_name"]
        description = request.form["description"]

        query = """
        UPDATE departments
        SET department_name=%s,
            description=%s
        WHERE department_id=%s
        """

        cursor.execute(
            query,
            (department_name, description, department_id)
        )

        db.commit()
        cursor.close()

        return redirect("/departments")

    cursor.execute(
        "SELECT * FROM departments WHERE department_id=%s",
        (department_id,)
    )

    department = cursor.fetchone()
    cursor.close()

    return render_template(
        "departments/edit.html",
        department=department
    )


@app.route("/departments/delete/<int:department_id>")
def delete_department(department_id):

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM departments WHERE department_id=%s",
        (department_id,)
    )

    db.commit()
    cursor.close()

    return redirect("/departments")

@app.route("/billing/add", methods=["GET", "POST"])
def add_bill():

    if request.method == "POST":

        patient_id = request.form["patient_id"]
        consultation_fee = request.form["consultation_fee"]
        medicine_fee = request.form["medicine_fee"]
        room_charge = request.form["room_charge"]
        other_charges = request.form["other_charges"]
        bill_date = request.form["bill_date"]

        total_amount = (
            float(consultation_fee or 0)
            + float(medicine_fee or 0)
            + float(room_charge or 0)
            + float(other_charges or 0)
        )

        cursor = db.cursor()

        query = """
        INSERT INTO billing
        (patient_id, consultation_fee, medicine_fee,
         room_charge, other_charges, total_amount, bill_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            patient_id,
            consultation_fee,
            medicine_fee,
            room_charge,
            other_charges,
            total_amount,
            bill_date
        )

        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return redirect("/billing")

    return render_template("billing/add.html")

@app.route("/billing")
def billing():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM billing
        ORDER BY bill_id DESC
    """)

    bills = cursor.fetchall()

    cursor.close()

    return render_template(
        "billing/list.html",
        bills=bills
    )

@app.route("/billing/edit/<int:bill_id>", methods=["GET", "POST"])
def edit_bill(bill_id):

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        patient_id = request.form["patient_id"]
        consultation_fee = request.form["consultation_fee"]
        medicine_fee = request.form["medicine_fee"]
        room_charge = request.form["room_charge"]
        other_charges = request.form["other_charges"]
        bill_date = request.form["bill_date"]

        total_amount = (
            float(consultation_fee or 0)
            + float(medicine_fee or 0)
            + float(room_charge or 0)
            + float(other_charges or 0)
        )

        query = """
        UPDATE billing
        SET patient_id=%s,
            consultation_fee=%s,
            medicine_fee=%s,
            room_charge=%s,
            other_charges=%s,
            total_amount=%s,
            bill_date=%s
        WHERE bill_id=%s
        """

        values = (
            patient_id,
            consultation_fee,
            medicine_fee,
            room_charge,
            other_charges,
            total_amount,
            bill_date,
            bill_id
        )

        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return redirect("/billing")

    cursor.execute(
        "SELECT * FROM billing WHERE bill_id=%s",
        (bill_id,)
    )

    bill = cursor.fetchone()
    cursor.close()

    return render_template(
        "billing/edit.html",
        bill=bill
    )


@app.route("/billing/delete/<int:bill_id>")
def delete_bill(bill_id):

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM billing WHERE bill_id=%s",
        (bill_id,)
    )

    db.commit()
    cursor.close()

    return redirect("/billing")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))