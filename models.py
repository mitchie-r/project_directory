from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column('Date', db.DateTime())
    title = db.Column('Title', db.String())
    description = db.Column('Short Description', db.String())
    skills = db.Column('Skills Practiced', db.String())
    url = db.Column('GitHub link', db.String())

    def __repr__(self):
        return f'''<Title: {self.title} Description: {self.description}
                    Skills: {self.skills} Link: {self.link}>'''
    
    
