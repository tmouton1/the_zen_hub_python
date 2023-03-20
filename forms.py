from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,TextAreaField,BooleanField
from wtforms.validators import DataRequired, Length
from model import Project


class ProjectForm(FlaskForm):
    projectname = StringField('project name', validators=[DataRequired(), Length(min=4, max=255)])
    description = TextAreaField('description')
    submit = SubmitField("submit")


class PoseForm(FlaskForm):
    posename = StringField('posename', validators=[DataRequired(), Length(min=4, max=255)])
    submit = SubmitField("submit")


    def update_projects(self, projects):
        self.project_selection.choices = [ (project.project_id, project.projectname) for project in projects ]
