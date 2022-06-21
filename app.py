from datetime import datetime

from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

import forms

app = Flask(__name__)
app.config["SECRET_KEY"] = "somesecret"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"{self.title} created on {self.date}"


@app.route("/index")
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = forms.AddTaskForm()
    if form.validate_on_submit():
        t = Task(title=form.title.data, date=datetime.utcnow())
        db.session.add(t)
        db.session.commit()
        print("Submitted title", form.title.data)
        flash("Task added to the database")
        return redirect(url_for("index"))
    return render_template("add.html", form=form)


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit(task_id):
    task = Task.query.get(task_id)
    form = forms.AddTaskForm()
    if task:
        if form.validate_on_submit():
            task.title = form.title.data
            task.date = datetime.utcnow()
            db.session.commit()
            flash("Task has been updated")
            return redirect(url_for("index"))

        form.title.data = task.title
        return render_template("edit.html", form=form, task_id=task_id)
    else:
        flash("Task not found")
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["GET", "POST"])
def delete(task_id):
    task = Task.query.get(task_id)
    form = forms.DeleteTaskForm()
    if task:
        if form.validate_on_submit():
            db.session.delete(task)
            db.session.commit()
            flash("Task has been deleted")
            return redirect(url_for("index"))

        return render_template(
            "delete.html", form=form, task_id=task_id, title=task.title
        )
    flash("Task does not exist")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
