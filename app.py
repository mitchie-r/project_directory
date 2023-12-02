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

@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

@app.route('/projects/new', methods=['GET', 'POST'])
def add_project():
    if request.form:
        new_project = Project(title=request.form['title'], date=request.form['date'],
                               description=request.form['desc'], skills=request.form['skills'],
                               link = request.form['github'])
        new_project.date = clean_date(new_project.date)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('index'))     
    return render_template('new.html')

@app.route('/project/<id>')
def detail(id):
    project = Project.query.get(id)
    return render_template('detail.html', project=project)

@app.route('/about')
def about():
    return render_template('about.html')




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=7000, host='127.0.0.1')