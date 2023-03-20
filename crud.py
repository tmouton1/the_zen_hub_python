from model import db, User, Project, Pose, Rating, connect_to_db


def create_user(username,email, password):
       
       user = User(username=username, email=email, password=password)

       return user

def all_users():
       
       return User.query.all()


def get_user_by_user_id(user_id):
       return User.query.get(user_id)



def get_user_by_email(email):
       
       return User.query.filter(User.email == email).first()


def create_project(user_id,projectname, description):
       project = Project(user_id=user_id,projectname=projectname, description=description)


       return project


def get_projects():

    return Project.query.all()



def get_project_by_id(project_id):
       return Project.query.get(project_id)

def get_pose_by_id(pose_id):
      return Pose.query.get(pose_id)

def create_pose(posename):
      pose = Pose(posename=posename)

      return pose

# def get_poses():
#       return Pose.query.all()






def create_rating(user, project, score):
       rating = Rating(user=user, project=project, score=score)

       return rating


def update_rating(rating_id, new_score):

    rating = Rating.query.get(rating_id)
    rating.score = new_score



def get_rating(user_id, rating_id):
    user_id = User.query.get()
    rating = Rating.query.get()

    return rating


if __name__ == '__main__':
    from server import app
    connect_to_db(app)


