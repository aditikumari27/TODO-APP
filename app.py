from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime   


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
         sno = db.Column(db.Integer, primary_key=True)
         title = db.Column(db.String(100))
         email = db.Column(db.String(100))
         date_created = db.Column(db.DateTime, default=datetime.utcnow)
     
         def __repr__(self) -> str:
              return f"{self.sno} - {self.title}"
    
    

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        email = request.form['email']
        todo = Todo(title=title, email=email)
        db.session.add(todo)
        db.session.commit() 

    return render_template("index.html", allTodo=Todo.query.all())

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if request.method == 'POST':
        title = request.form['title']
       # desc = request.form['desc']
        email = request.form['email']
        todo = Todo(title=title, email=email)
        db.session.add(todo)
        db.session.commit() 
        
    return render_template("todo.html", allTodo=Todo.query.all())
    

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        email = request.form['email']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.email = email
        db.session.add(todo)
        db.session.commit() 
        return redirect("/todo")
    else:
        todo = Todo.query.filter_by(sno=sno).first()    
        return render_template("update.html", todo=todo)


@app.route('/delete/<int:sno>', methods=['POST', 'GET'])
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return "Todo with sno has been deleted successfully!"



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

