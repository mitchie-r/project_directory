from flask import (render_template, url_for,
                   request, redirect)

from models import db, app, Project

import datetime

# Cleans the date entry to a datetime that can be added to the db


def clean_date(date):
    date_split = date.split('/')
    month = int(date_split[0])
    day = int(date_split[1])
    year = int(date_split[2])
    datetime_val = datetime.datetime(year, month, day)
    return datetime_val

# Cleans the entry during editing a db entry


def clean_date_edit(datetime_val):
    datetime_string = datetime_val
    datetime_object = datetime.datetime.strptime(
        datetime_string, "%Y-%m-%d %H:%M:%S")
    return datetime_object

# To list skills on  main page and not repeat entries


def clean_skills(projects):
    combined_skills = []
    new_comb_skills = []
    for project in projects:
        combined_skills.append(project.skills)
    conv_skills = ",".join(combined_skills)
    combined_skills = list(conv_skills.split(","))
    for skill in combined_skills:
        skill = skill.rstrip("\r\n")
        skill = skill.lstrip("and ")
        skill = skill.strip()
        if skill in new_comb_skills:
            continue
        else:
            new_comb_skills.append(skill)
    print(new_comb_skills)
    #new_comb_skills = ", ".join(new_comb_skills)
    return new_comb_skills

# index route root


@app.route('/')
def index():
    projects = Project.query.all()
    combined_skills = clean_skills(projects)
    return render_template('index.html', projects=projects, combined_skills=combined_skills)

# route to add a project


@app.route('/projects/new', methods=['GET', 'POST'])
def add_project():
    projects = Project.query.all()
    if request.form:
        new_project = Project(title=request.form['title'], date=request.form['date'],
                              description=request.form['desc'], skills=request.form['skills'],
                              url=request.form['github'])
        new_project.date = clean_date(new_project.date)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new.html', projects=projects)

# route to an individual project's detailed view


@app.route('/projects/<id>')
def detail(id):
    projects = Project.query.all()
    project = Project.query.get_or_404(id)
    skills = list((project.skills).split(","))            
    return render_template('detail.html', project=project, projects=projects, skills=skills)

# route to edit an individual project


@app.route('/projects/<id>/edit', methods=['GET', 'POST'])
def edit_project(id):
    projects = Project.query.all()
    project = Project.query.get_or_404(id)
    if request.form:
        project.title = request.form['title']
        project.date = request.form['date']
        project.date = clean_date_edit(project.date)
        project.description = request.form['desc']
        project.skills = request.form['skills']
        project.url = request.form['github']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', project=project, projects=projects)

# route to delete project


@app.route('/projects/<id>/delete')
def delete_project(id):
    project = Project.query.get(id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('index'))

# route to the about page


@app.route('/about')
def about():
    projects = Project.query.all()
    return render_template('about.html', projects=projects)

# handles page not found errors iwth a custom view


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', msg=error), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=7000, host='127.0.0.1')
