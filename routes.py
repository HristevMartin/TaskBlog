from app import *


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("add.html")
