from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


#Using Flask SQL for creating a model with this class below
class Todo(db.Model):
    #Creating ID for the table(Model) that ll'be save it.
    id = db.Column(db.Integer,  primary_key= True) 
    # It is a content that will be saved
    content = db.Column(db.String(200), nullable=False)
    # And this is time.
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# This is the way todo some action
@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task!'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

# This is the way todo some action
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()

        return redirect('/')
    except:
        return 'That was a problem deleting that task! :c'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content= request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Sorry! There was issue updating your task. '
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)