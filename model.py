from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()




class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    project = db.relationship("Project", back_populates="user", lazy="dynamic")
    pose = db.relationship("Pose", back_populates="user", lazy="dynamic" )
   
    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email} username={self.username}>"
    

class Project(db.Model):
    __tablename__ = "projects"

    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    projectname = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), unique=False, nullable=False) 
    user = db.relationship("User", back_populates="project")
    pose = db.relationship("Pose", back_populates="project", lazy="dynamic")
    pose_id = db.relationship("Pose", back_populates="project", lazy="dynamic")
    posename = db.relationship("Pose", back_populates="project", lazy="dynamic")

    rating = db.relationship("Rating", back_populates="project", lazy="dynamic")

    def __repr__(self):
        return f"<Project project_id={self.project_id} projectname={self.projectname}>"
    

class Pose(db.Model):
    __tablename = "poses"

    pose_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    posename = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False) 
    user = db.relationship("User", back_populates="pose") 
    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_id"), nullable=False) 
    project = db.relationship("Project", back_populates="pose") 
    

    def __repr__(self):
        return f"<Pose pose_id={self.pose_id} description={self.description} posename={self.posename}>"

class Rating(db.Model):
    """A project rating."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_id"))
    project = db.relationship("Project", back_populates="rating")
    
    def __repr__(self):
        return f"<Rating rating_id={self.rating_id} score={self.score}>"
    

    

def connect_to_db(flask_app,db_uri=os.environ['DATABASE_URI'], echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)



print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    
    connect_to_db(app)