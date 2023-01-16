from flask_wtf import FlaskForm
from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf.recaptcha import RecaptchaField
from wtforms import SubmitField

app = Flask(__name__)
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfZPf8jAAAAAIY9bVq6OnZHhJ1sFsIcR6iyh6-i'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfZPf8jAAAAANQB0l37iAmrLw4jUv8Le5lL_A-L'


class RegisterForm(FlaskForm):
    recaptcha = RecaptchaField()
    submit = SubmitField('Sign Up')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Do registration
        pass
    return render_template('register.html', form=form)

app.run(debug=True)