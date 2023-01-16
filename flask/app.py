from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import encode_decode
import ssl

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'kriptomail-mysql.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'yagizdeniz'
app.config['MYSQL_PASSWORD'] = 'MIIG5QIBAAKCAYEAz2/efvljGpJW9yMKrH2g2wtvlm+loTCohY7wYXqNW9ZloxbA'
app.config['MYSQL_DB'] = 'login'

mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = encode_decode.encode(request.form['password'])
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE email = % s AND password = % s', (email, password))
        hesap = cursor.fetchone()

        if hesap:
            session['loggedin'] = True
            session['email'] = hesap['email']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        password = encode_decode.encode(request.form['password'])
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        sql = 'SELECT * FROM login WHERE email = %(mail)s'
        girilenler = {
            'mail': email,
        }

        cursor.execute(sql, girilenler)

        hesap = cursor.fetchone()
        cursor.execute('INSERT INTO login VALUES (% s, % s)', (password, email))
        mysql.connection.commit()
        msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_verify_locations("/home/kriptomail/root.pem")
context.load_cert_chain("/home/kriptomail/a.pem", "/home/kriptomail/kriptomail.me.key")


app.run(debug=True,ssl_context=context,host='0.0.0.0',port=443)
