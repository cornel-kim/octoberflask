from flask import Flask, render_template, request, session
import pymysql

app = Flask(__name__)
app.secret_key = '12sek'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/viewuser')
def viewuser():
    if 'logged' in session:

        conn = pymysql.connect("localhost", "root", "", "oct_class")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM register_user WHERE username = %s ", (session['username']))
        result = cursor.fetchone()
        return render_template("view_user.html", result=result)
    else:
        return render_template("view_user.html", msg="no user found")


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        firstname = request.form['firstname']
        lastname= request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        conn = pymysql.connect("localhost", "root", "", "oct_class")
        cursor = conn.cursor()
        sql = "INSERT INTO register_user (username, firstname, lastname, email, password) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (username, firstname, lastname, email, password))
        conn.commit()
        return render_template("login.html")
    else:
       return render_template("register.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = pymysql.connect("localhost", "root", "", "oct_class")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM register_user WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        if result:
            session['logged'] = True
            session['username'] = result[0]
            msg = 'logged in successfully'
            return render_template("view_user.html", result=result)
        else:
            msg = 'please input valid details'
            return render_template("login.html")
    else:
        return render_template("login.html", msg = "No user found")


@app.route('/gallery')
def gallery():
    return render_template("gallery.html")


@app.route('/branches')
def branches():
    return render_template("branches.html")


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        email = request.form['email']
        phone_number = request.form['phone_number']
        msg = request.form['msg']

        conn = pymysql.connect("localhost", "root", "", "oct_class")
        cursor = conn.cursor()
        sql = "INSERT INTO contact_tbl (email, phone_number, msg) VALUES (%s, %s, %s)"
        cursor.execute(sql, (email, phone_number, msg))
        conn.commit()
        return render_template("index.html")
    else:
        return render_template("contact.html")


@app.route('/view')
def view():
    conn = pymysql.connect("localhost", "root", "", "oct_class")
    cursor = conn.cursor()
    select_query = "SELECT * FROM contact_tbl"
    cursor.execute(select_query)
    if cursor.rowcount<1:
        return render_template("view_contact.html", msg = "No records found")
    else:
        rows = cursor.fetchall()
        return render_template("view_contact.html", rows=rows)


if __name__ == '__main__':
    app.debug = True
    app.run()

