from flask import (render_template, url_for,
                   request, redirect)

from models import db, app, Project

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add-project', methods=['GET', 'POST'])
def add_project():
    if request.form:
        new_project = Project(title=request.form['title'], date=request.form['date'],
                               description=request.form['desc'], skills=request.form['skills'],
                               link = request.form['github'])
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('index'))     
    return render_template('addproject.html')
        
        # new_project.name
        # new_project.skills
        # db.session.add(new_project )
        # db.session.commit()
        
    #return render_template('addproject.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=7000, host='127.0.0.1')