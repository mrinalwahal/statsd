# Statsd Tutorial Application
# Author: Mrinal Wahal


# import dependencies
from flask import Flask, request
from flask import render_template
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

import time
import statsd

# connect statsd client
c = statsd.StatsClient('localhost',8125)

# start flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# initiate DB
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)

    def __init__(self, content):
        self.content = content
        self.done = False

db.create_all()


@app.route('/')
def tasks_list():
    tasks = Task.query.all()

@app.route('/task', methods=['POST'])
def add_task():
    start=time.time()
    content = request.form['content']
    if not content:
    	dur = (time.time() - start) *1000
    	c.timing("errortime",dur)
    	c.incr("errorcount")
        return 'Error'

    task = Task(content)
    db.session.add(task)
    db.session.commit()
    dur = (time.time() - start) *1000
    c.timing("tasktime",dur)
    c.incr("taskcount")


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    c.incr("deletecount")


@app.route('/done/<int:task_id>')
def resolve_task(task_id):
    task = Task.query.get(task_id)
    if task.done:
        task.done = False
    else:
        task.done = True

    db.session.commit()


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=8888)
