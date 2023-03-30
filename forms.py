from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField, SelectField
from wtforms.validators import DataRequired, Length


class ProjectForm(FlaskForm):
    projectname = StringField('project name', validators=[DataRequired(), Length(min=4, max=255)])
    description = TextAreaField('description')
    submit = SubmitField("submit")


class PoseForm(FlaskForm):
    posename = StringField('posename', validators=[DataRequired(), Length(min=4, max=255)])
    # project_selection = SelectField("project") 
    submit = SubmitField("submit")

    # def update_project(self, projects):
    #     self.project_selection.choices =  [(projects.id, projects.projectname) for projects in projects] 
   