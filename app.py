from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "campusos_secret_key"

# Database setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///campus.db"
db = SQLAlchemy(app)


# -----------------------------
# Database Models
# -----------------------------

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    date = db.Column(db.String(50))
    description = db.Column(db.String(200))


class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    message = db.Column(db.String(200))


class StudyMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100))
    title = db.Column(db.String(100))
    link = db.Column(db.String(300))


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    message = db.Column(db.String(500))

class AcademicCalendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    date = db.Column(db.String(50))
    description = db.Column(db.String(200))

class Placement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100))
    role = db.Column(db.String(100))
    eligibility = db.Column(db.String(100))
    last_date = db.Column(db.String(50))
    apply_link = db.Column(db.String(300))


# -----------------------------
# Home
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Student Registration
# -----------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        student = Student(
            name=name,
            email=email,
            password=password
        )

        db.session.add(student)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


# -----------------------------
# Student Login
# -----------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        student = Student.query.filter_by(
            email=email,
            password=password
        ).first()

        if student:
            session["student_id"] = student.id
            return redirect("/dashboard")

        return "Invalid Login"

    return render_template("login.html")


# -----------------------------
# Dashboard
# -----------------------------

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/profile")
def profile():

    student = Student.query.get(session["student_id"])

    return render_template("profile.html", student=student)


# -----------------------------
# Events
# -----------------------------

@app.route("/events")
def events():

    all_events = Event.query.all()

    return render_template("events.html", events=all_events)


# -----------------------------
# Notices
# -----------------------------

@app.route("/notices")
def notices():

    all_notices = Notice.query.all()

    return render_template("notices.html", notices=all_notices)


# -----------------------------
# Study Materials
# -----------------------------

@app.route("/study_materials")
def study_materials():

    materials = StudyMaterial.query.all()

    return render_template("study_materials.html", materials=materials)

@app.route("/placements")
def placements():

    placements = Placement.query.all()

    return render_template("placements.html", placements=placements)




# -----------------------------
# Logout
# -----------------------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# -----------------------------
# Admin Login
# -----------------------------

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":

            session["admin"] = True
            return redirect("/admin")

        else:
            return "Invalid Admin Login"

    return render_template("admin_login.html")
# -----------------------------
# Admin Panel
# -----------------------------

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if "admin" not in session:
        return redirect("/admin_login")

    if request.method == "POST":

        form_type = request.form["type"]

        if form_type == "event":

            title = request.form["title"]
            date = request.form["date"]
            description = request.form["description"]

            event = Event(
                title=title,
                date=date,
                description=description
            )

            db.session.add(event)
            db.session.commit()

            return "Event Added Successfully"

        elif form_type == "notice":

            title = request.form["title"]
            message = request.form["message"]

            notice = Notice(
                title=title,
                message=message
            )

            db.session.add(notice)
            db.session.commit()

            return "Notice Added Successfully"
        elif form_type == "placement":

          company = request.form["company"]
          role = request.form["role"]
          eligibility = request.form["eligibility"]
          last_date = request.form["last_date"]
          apply_link = request.form["apply_link"]

        placement = Placement(
           company=company,
           role=role,
           eligibility=eligibility,
           last_date=last_date,
           apply_link=apply_link
        )

        db.session.add(placement)
        db.session.commit()

    return "Placement Added Successfully"

    return render_template("admin.html")


# -----------------------------
# Add Study Material
# -----------------------------

@app.route("/add_material", methods=["POST"])
def add_material():

    if "admin" not in session:
        return redirect("/admin_login")

    subject = request.form["subject"]
    title = request.form["title"]
    link = request.form["link"]

    material = StudyMaterial(
        subject=subject,
        title=title,
        link=link
    )

    db.session.add(material)
    db.session.commit()

    return "Study Material Added Successfully"
@app.route("/add_calendar", methods=["POST"])
def add_calendar():

    if "admin" not in session:
        return redirect("/admin_login")

    title = request.form["title"]
    date = request.form["date"]
    description = request.form["description"]

    calendar = AcademicCalendar(
        title=title,
        date=date,
        description=description
    )

    db.session.add(calendar)
    db.session.commit()

    return "Calendar Event Added Successfully"

@app.route("/add_placement", methods=["POST"])
def add_placement():

    if "admin" not in session:
        return redirect("/admin_login")

    company = request.form["company"]
    role = request.form["role"]
    eligibility = request.form["eligibility"]
    last_date = request.form["last_date"]
    apply_link = request.form["apply_link"]

    placement = Placement(
        company=company,
        role=role,
        eligibility=eligibility,
        last_date=last_date,
        apply_link=apply_link
    )

    db.session.add(placement)
    db.session.commit()

    return "Placement Added Successfully"

# -----------------------------
# Demo Routes
# -----------------------------

@app.route("/add_event")
def add_event():

    event = Event(
        title="Hackathon 2026",
        date="15 July 2026",
        description="Build innovative projects and compete."
    )

    db.session.add(event)
    db.session.commit()

    return "Event Added"


@app.route("/add_notice")
def add_notice():

    notice = Notice(
        title="Exam Notice",
        message="Semester examination schedule has been released."
    )

    db.session.add(notice)
    db.session.commit()

    return "Notice Added"
# -----------------------------
# Feedback
# -----------------------------

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")


@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():

    name = request.form["name"]
    message = request.form["message"]

    feedback = Feedback(
        name=name,
        message=message
    )

    db.session.add(feedback)
    db.session.commit()

    return "Feedback Submitted Successfully!"


# -----------------------------
# Admin Feedback
# -----------------------------

@app.route("/admin_feedback")
def admin_feedback():

    if "admin" not in session:
        return redirect("/admin_login")

    feedbacks = Feedback.query.all()

    return render_template("admin_feedback.html", feedbacks=feedbacks)

@app.route("/calendar")
def calendar():

    calendars = AcademicCalendar.query.all()

    return render_template("calendar.html", calendars=calendars)

@app.route("/search")
def search():

    query = request.args.get("query")

    events = Event.query.filter(
        Event.title.contains(query)
    ).all()

    notices = Notice.query.filter(
        Notice.title.contains(query)
    ).all()

    materials = StudyMaterial.query.filter(
        StudyMaterial.title.contains(query)
    ).all()

    placements = Placement.query.filter(
        Placement.company.contains(query)
    ).all()

    return render_template(
        "search.html",
        query=query,
        events=events,
        notices=notices,
        materials=materials,
        placements=placements
    )
# -----------------------------
# AI Campus Assistant
# -----------------------------

@app.route("/ai_assistant", methods=["GET", "POST"])
def ai_assistant():

    answer = None

    if request.method == "POST":

        question = request.form["question"].lower()

        if "event" in question:
            answer = "You can check upcoming events in the Events section."

        elif "notice" in question:
            answer = "Latest campus notices are available in the Notices section."

        elif "study" in question or "material" in question:
            answer = "Study materials are available in the Study Materials section."

        elif "placement" in question or "job" in question:
            answer = "Placement opportunities are available in the Placement section."

        elif "calendar" in question or "exam" in question:
            answer = "Academic dates and exam schedules are available in the Academic Calendar."

        else:
            answer = "I can help you with Events, Notices, Study Materials, Placements and Academic Calendar."

    return render_template(
        "ai_assistant.html",
        answer=answer
    )

# -----------------------------
# Run App
# -----------------------------

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)

