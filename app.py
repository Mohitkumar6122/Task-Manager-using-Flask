# BASIC TASK MANAGER APP USING FLASK 
# DEVELOPER : MOHIT KUMAR

from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model) :
  id = db.Column(db.Integer, primary_key = True)
  content = db.Column(db.String(200), nullable = False)
  date_created = db.Column(db.DateTime, default = datetime.utcnow) 
  
  def __repr__(self) :
    return '<Task %r>' % self.id

@app.route('/', methods = ['GET', 'POST'])
def index():
  if request.method =='POST' :
    task_content = request.form['content']
    new_task = Todo(content = task_content)
    # return task_content
    try :   
      db.session.add(new_task)
      db.session.commit()
      return redirect('/')
    except :
      return "Error in adding task please try again ...!"
  else :
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template("index.html", tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
  task_to_delete = Todo.query.get_or_404(id)
  
  try :
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')
  except :
    return "There was a problem in deleting task please try again ...!"

@app.route('/update/<int:id>', methods =['GET', 'POST'])
def update(id):
  task = Todo.query.get_or_404(id)
  
  if request.method =='POST' :
    task.content = request.form['content']
    try :
      db.session.commit()
      return redirect('/')
    except :
      return 'There was a problem in updating task please try again ...!'
  else :
    return render_template('update.html', task = task)
  
@app.route('/about')
def about():
  return render_template('about.html', title = about)

if __name__ == "__main__" :
  app.run(debug = True)  