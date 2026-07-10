
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "campusos_secret_key"

# Database setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///campus.db"
db = SQLAlchemy(app)


# Student table
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


@app.route("/")
def home():
    return render_template("index.html")


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

        else:
            return "Invalid Login"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/profile")
def profile():

    student = Student.query.get(session["student_id"])

    return render_template("profile.html", student=student)


@app.route("/events")
def events():

    all_events = Event.query.all()

    return render_template("events.html", events=all_events)

@app.route("/notices")
def notices():

    all_notices = Notice.query.all()

    return render_template("notices.html", notices=all_notices)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

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

@app.route("/admin", methods=["GET", "POST"])
def admin():

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


    return render_template("admin.html")
    return render_template("admin.html")


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)
