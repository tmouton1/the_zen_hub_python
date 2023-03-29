from flask import Flask
from flask import Flask, render_template, url_for, request, flash, session,redirect
from model import connect_to_db, db, Pose, User
import crud
from forms import PoseForm, ProjectForm

from jinja2 import StrictUndefined

app = Flask(__name__)

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def home():
    "view homepage"
    return render_template("home.html")


# ======================================================

@app.route("/projects")
def all_projects():
    """View all projects."""

    
    project = crud.get_projects()


    return render_template("projects.html", project=project)

# ===============================

@app.route("/login", methods=["POST"])
def user_login():

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        session["user_email"] = user.email

        flash(f"Welcome back, {user.email}!")

    return redirect("/")

# =======================================================

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    username=request.form.get("username")
    email=request.form.get("email")
    password=request.form.get("password")


    user = crud.get_user_by_email(email)
    if user:
        flash("This email already exists, please try another.")
    else:
        user = crud.create_user(username,email, password)
        with app.app_context():
                db.session.add(user)
                db.session.commit()

                flash("Account has been created successfully, Please login.")

    return redirect("/")

# =======================================================


@app.route("/users")
def all_users():
    """View all users."""

    users = crud.all_users()

    return render_template("users.html", users=users)

# ========================================================

@app.route("/users/<user_id>")
def show_user(user_id):

    user = crud.get_user_by_user_id(user_id)

    return render_template("/user_profile.html",user=user)

# ====================================================

@app.route("/add_project", methods=['GET','POST'])
def add_project():

    "add new project"
    logged_in_email = session.get("user_email")
    
    projectname = request.form.get("projectname")
    description = request.form.get("description")


    if logged_in_email is None:
        flash("Please login to create your project.")
    else:
        user = crud.get_user_by_email(logged_in_email)

        new_project = crud.create_project(projectname,description,user.user_id)

        with app.app_context():
            db.session.add(new_project)
            db.session.commit()


            flash(f"Thank you for adding {projectname}! Let's add some poses.")

            return redirect(f"/users/{user.user_id}")


    # ===========================================

@app.route("/add_pose/pose_id>", methods=['GET','POST'])
def add_pose():
    "add new pose"

    project = crud.get_project_by_id()
    logged_in_email = session.get("user_email")

    posename = request.form.get("posename")

    if logged_in_email is None:
        flash("Please login to create your project.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        new_pose = crud.create_pose(posename)

        with app.app_context():
            db.session.add(new_pose)
            db.session.commit()

  
        flash(f"Thank you for adding {posename}!")

        return redirect(f"project_details/ {project.project_id}")
# -=========================================================


@app.route("/projects/<project_id>")
def show_project(project_id):

    project = crud.get_project_by_id(project_id)
    
    pose_form = PoseForm()

    return render_template("/project_details.html",project=project, pose_form=pose_form)
# =================================================


@app.route("/projects/<project_id>", methods=["POST"])
def create_rating(project_id):
    """Create a new rating for the movie."""

    logged_in_email = session.get("user_email")
    score = request.form.get("rating")

    if logged_in_email is None:
        flash("Please login to rate a movie.")
    elif not score:
        flash("Error: you didn't select a score for your rating.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        project = crud.get_project_by_id(project_id)

        rating = crud.create_rating(project, int(score))

        db.session.add(rating)
        db.session.commit()
        

        flash(f"You rated this sequence {score} out of 5.")

    return redirect(f"/projects/{project_id}")


@app.route("/update_rating", methods=["POST"])
def update_rating():
    rating_id = request.json["rating_id"]
    new_score = request.json["updated_score"]
    crud.update_rating(rating_id, new_score)
    
    with app.app_context():
        db.session.add(new_score)
        db.session.commit()

#     return "Success"

# @app.route("/projects/<pose_id>")
# def show_pose(pose_id):

#     pose = crud.get_pose_by_id(pose_id)

#     return render_template("/project_details.html",pose=pose)





if __name__ == "__main__":
        connect_to_db(app)
        app.env = "development"
        app.run(debug = True, port = 8000, host = "localhost")
