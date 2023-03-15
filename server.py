from flask import Flask
from flask import Flask, render_template, url_for, request, flash, session,redirect
from model import connect_to_db, db, Project, User
import crud
from forms import ProjectForm

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

# ======================================================

# @app.route("/projects/<project_id>")
# def show_project(project_id):
     
#     new_project = crud.get_project_by_id(project_id)
    

    # return render_template("project_details.html", new_project=new_project)

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

    return render_template("user_profile.html",user=user)

# ====================================================


@app.route("/add_project", methods=['GET','POST'])
def add_project():
    "add new project"

    # projectname = False

    # form = ProjectForm()
    # if form.validate_on_submit():

    #     projectname = False
    #     description = False

    #     projectname = form.projectname.data
    #     description = form.description.data
    #     form.projectname.data = ''
    #     form.description.data = ''



    #     return render_template('user_profile.html', projectname=projectname, description=description, form=form)




    
    logged_in_email = session.get("user_email")
    projectname = request.form.get("projectname")
    description = request.form.get("description")
    

    if logged_in_email is None:
        flash("Please login to create your project.")
    else:
        user = crud.get_user_by_email(logged_in_email)
    
        new_project = crud.create_project(projectname,description)

        with app.app_context():

            db.session.add(new_project)
            db.session.commit()
        
            flash(f"Thank you for adding project, {new_project}! Let's add some poses.")

            return redirect(f"/user_profile/, {projectname}, {description}")
   

    # ===========================================

@app.route("/users/rating")
def show_rating(score):
     
    rating = crud.get_rating(score)
    with app.app_context():
        db.session.append(rating)
        db.session.commit()

    return render_template("user_profile.html",score=score)

# =================================================
@app.route("/projects/<project_id>", methods=["POST"])
def create_rating(project_id):
    """Create a new rating for the project."""

    logged_in_email = session.get("user_email")
    rating_score = request.form.get("rating")

    if logged_in_email is None:
        flash("Please login to rate this project.")
    elif not rating_score:
        flash("Error: you didn't select a score for your rating.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        project = crud.get_project_by_id(project_id)

        rating = crud.create_rating(user, project, int(rating_score))

        with app.app_context():

            db.session.add(rating)
            db.session.commit()
        
            flash(f"You rated this movie {rating_score} out of 5.")

            return redirect(f"/projects/{project_id}")
   


if __name__ == "__main__":
        connect_to_db(app)
        app.env = "development"
        app.run(debug = True, port = 8000, host = "localhost")



