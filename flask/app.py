import requests
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
app = Flask(__name__)
@app.route('/register', methods=['POST'])
def register():
    # Get the reCAPTCHA response
    response = request.form['g-recaptcha-response']

    # Verify the reCAPTCHA response
    secret_key = '6LfZPf8jAAAAANQB0l37iAmrLw4jUv8Le5lL_A-L'
    url = 'https://www.google.com/recaptcha/api/siteverify'
    data = {'secret': secret_key, 'response': response}
    result = requests.post(url, data=data)

    if result.json()['success']:
        # The reCAPTCHA was successfully verified
        # Continue with your registration logic
        pass
    else:
        # The reCAPTCHA was not successfully verified
        # Return an error message or redirect the user to an error page
        pass

app.run(debug=True,host='0.0.0.0',port=443)
