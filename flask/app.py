from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import encode_decode


RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = '6LcUv_8jAAAAAFVhpFC0zM-4OxVD04T7nxcPxSCI'
RECAPTCHA_PRIVATE_KEY = '6LcUv_8jAAAAAGsvX2cnLj7QRKD8v3gtsp8DBFlB'
RECAPTCHA_OPTIONS = {'theme': 'white'}

app = Flask(__name__)
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LcUv_8jAAAAAFVhpFC0zM-4OxVD04T7nxcPxSCI'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LcUv_8jAAAAAGsvX2cnLj7QRKD8v3gtsp8DBFlB'
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}


class RegisterForm(FlaskForm):
    recaptcha = RecaptchaField()
    submit = SubmitField('Sign Up')


app = Flask(__name__)

app.secret_key = '6LfZPf8jAAAAANQB0l37iAmrLw4jUv8Le5lL_A-L'

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
    form = RegisterForm()
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form and form.validate_on_submit():
        password = encode_decode.encode(request.form['password'])
        email = request.form['email']

        safequestion1 = request.form['safequestion1']
        safeanswer1 = encode_decode.encode(request.form['safeanswer1'])

        safequestion2 = request.form['safequestion2']
        safeanswer2 = encode_decode.encode(request.form['safeanswer2'])

        safequestion3 = request.form['safequestion3']
        safeanswer3 = encode_decode.encode(request.form['safeanswer3'])

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        sql = 'SELECT * FROM login WHERE email = %(mail)s'
        girilenler = {
            'mail': email,
        }

        cursor.execute(sql, girilenler)

        hesap = cursor.fetchone()
        cursor.execute('INSERT INTO login VALUES (% s, % s, % s, % s, % s, % s, % s, % s)', (email, password, safequestion1, safeanswer1, safequestion2, safeanswer2, safequestion3, safeanswer3))
        mysql.connection.commit()
        msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg, form=form)


app.run(debug=True)
