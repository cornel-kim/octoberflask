from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


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


if __name__ == '__main__':
    app.run()
    app.debug(True)
