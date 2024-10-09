from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    is_done = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

id = 2
tasks = [
    {"id": 1, "title": "wash the dishes", "is_done": False},
    {"id": 2, "title": "finish homework", "is_done": False}
]

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return tasks

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    for task in tasks:
        if task['id']==task_id:
            return task
    return {'error': 'task not found'}

@app.route('/tasks', methods=['POST'])
def create_task():
    global id
    id+=1
    new_task={'id':id, 'title':request.json['title'], 'is_done':False}
    tasks.append(new_task)
    return new_task

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    for task in tasks:
        if task['id']==task_id:
            task['title'] = request.json['title']
            task['is_done'] = request.json['is_done']
            return task
    return {'error': 'task not found'}

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for task in tasks:
        if task['id']==task_id:
            tasks.remove(task)
            return task
    return {'error': 'task not found'}

if __name__ == '__main__':
    app.run(debug=True)