from flask import (render_template, url_for,
                   request, redirect)

from models import db, app, Project

import datetime

def clean_date(date):
    date_split= date.split('/')
    month = int(date_split[0])
    day = int(date_split[1])
    year = int(date_split[2])
    datetime_val = datetime.datetime(year, month, day)
    return datetime_val

def clean_date_edit(datetime_val):
    datetime_string = datetime_val
    datetime_object = datetime.datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
    return datetime_object

# converted_date = f"{month}/{day}/{year}"
@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

@app.route('/projects/new', methods=['GET', 'POST'])
def add_project():
    projects = Project.query.all()
    if request.form:
        new_project = Project(title=request.form['title'], date=request.form['date'],
                               description=request.form['desc'], skills=request.form['skills'],
                               link = request.form['github'])
        new_project.date = clean_date(new_project.date)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('index'))     
    return render_template('new.html', projects=projects)

@app.route('/projects/<id>')
def detail(id):
    projects = Project.query.all()
    project_id = Project.query.get(id)
    return render_template('detail.html', projects=projects, project_id=project_id)

@app.route('/projects/<id>/edit', methods=['GET', 'POST'])
def edit_project(id):
    projects = Project.query.all()
    project_id = Project.query.get(id)
    if request.form:
        project_id.title = request.form['title']
        project_id.date = request.form['date']
        project_id.date = clean_date_edit(project_id.date)
        project_id.description = request.form['desc']
        project_id.skills = request.form['skills']
        project_id.link = request.form['github']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editproject.html', project_id=project_id, projects=projects)

@app.route('/about')
def about():
    projects = Project.query.all()
    return render_template('about.html', projects=projects)




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=7000, host='127.0.0.1')