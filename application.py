from config import *


@app.route("/")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from post")
    result = cur.fetchall()
    return render_template("index.html", posts = result )



@app.route("/post/<string:id>/")
def post(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from post WHERE id=%s",[id])
    result = cur.fetchone()
    return render_template("post.html", posts=result)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")
