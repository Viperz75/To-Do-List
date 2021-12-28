from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import datetime

app = Flask(__name__)
app.secret_key = "ahf8u283614874901839145645145fa65s46a6f"
Bootstrap(app)
# DB (Data Base) Creation
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tasks.db"
# It will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Tables in DB
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), unique=True, nullable=False)
    category = db.Column(db.String(250), nullable=False)
    date = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)


# Creating DB
db.create_all()


# Routes to Site Pages
@app.route("/")
def home():
    # Receiving all data in the DB
    all_tasks = db.session.query(Tasks).all()
    time_now = datetime.datetime.now()
    time = time_now.strftime("%H:%M")
    print(time)
    return render_template("index.html", all=all_tasks, time=time)


@app.route("/add", methods=['GET', "POST"])
def add():
    if request.method == "POST":
        # Record Creation
        new_task = Tasks(
            task=request.form["task"],
            category=request.form["category"],
            date=request.form["date"],
            time=request.form["time"]
        )
        # Adding record
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/delete")
def delete():
    # DELETE A RECORD BY ID
    task_id = request.args.get('id')
    task_to_delete = Tasks.query.get(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
