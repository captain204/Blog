from config import *
from validators import *


@app.route("/register", methods=['GET','POST'])
def register():
    form = User(request.form)
    if request.method == "POST" and form.validate(): 
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(username, email, password)VALUES (%s, %s, %s)",(username,email,password))
        mysql.connection.commit()
        cur.close
        flash("Registration complete login","success")
        redirect(url_for("login"))
    return render_template("admin/register.html",form = form)


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method =="POST":
        username = request.form['username']
        password_candidate = request.form['password']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username=%s",[username])
        if result > 0:
            data = cur.fetchone()
            password = data["password"]
            id = data["id"]
            if sha256_crypt.verify(password_candidate,password):
                session['logged_in'] = True
                session['username'] = username
                session['id'] = id
                flash("You are currently logged in","success")
                return redirect(url_for('dashboard'))
            else:
                error = "Invalid login credentials"
                return render_template("admin/login.html", error = error)
        else:
            error = "User not found"
            return render_template("admin/login.html",error = error)
    return render_template("admin/login.html")

def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash("Unauthorized access please login","danger")
            return redirect(url_for('login'))
    return wrap

@app.route("/logout")
def logout():
    session.clear()
    flash("You are currently logged out","success")
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET','POST'])
@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from post")
    result = cur.fetchall()
    return render_template('admin/dashboard.html',post = result)

  
@app.route('/addPost', methods=['GET','POST'])
@is_logged_in
def addPost():
    form = Post(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        user_id = session['id']
        author = session['username']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO post (title, body, user_id, author) VALUES(%s, %s, %s, %s)",(title, body, user_id, author))
        mysql.connection.commit()
        cur.close()
        flash('Article created successfully','success')
    return render_template("admin/create.html", form=form)


@app.route("/update/<string:id>/", methods=['GET','POST'])
@is_logged_in
def update(id):
    
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * from post WHERE id=%s",[id])
    article =  cur.fetchone()
    form = Post(request.form)
    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        cur.execute("UPDATE post SET  title=%s, body = %s WHERE id =%s",(title,body,id))
        mysql.connection.commit()
        cur.close()
        flash("Article Updated","success")
        return redirect(url_for('dashboard'))

    return render_template("admin/update.html", post = result, form=form)


@app.route("/delete/<string:id>/",methods=['POST'])
@is_logged_in
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE from post WHERE id =%s", [id])
    mysql.connection.commit()
    cur.close()
    flash("Delete Completed","danger")
    return redirect(url_for('dashboard'))



if  __name__ == "__main__":
    app.run(debug=True)