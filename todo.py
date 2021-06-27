from logging import debug
from flask import Flask,render_template,url_for
from flask.globals import request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import url
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/user/Flask/todo/todo.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    complete = db.Column(db.Boolean)

@app.route("/")
def index():
    todos = Todo.query.all() # Todos bir directory 

    return render_template("index.html",todos = todos)

@app.route("/add",methods = ["POST"])
def addTodo():
    title = request.form.get("title")
    content = request.form.get("content")
    newTodo=Todo(title = title , content = content,complete=False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))
@app.route("/complete/<string:id>",methods=["GET"])
def completeTodo(id):  #BTN complete 
    todo = Todo.query.filter_by(id=id).first() # Tablodan ID si eşleşen veriyi al 
    if todo.complete == False:
        todo.complete = True
    else:
        todo.complete = False
    db.session.commit()  #Güncelle 
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id=id).first() # Tablodan ID si eşleşen veriyi al 
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))
@app.route("/detail/<string:id>")
def detailTodo(id):
    todo = Todo.query.filter_by(id=id).first() # Tablodan ID si eşleşen veriyi al 
    return render_template("detail.html",todo=todo)


if __name__ == "__main__":
    app.run(debug = True)
