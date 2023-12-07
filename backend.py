import os
import hashlib
import re

from flask import Flask, request, render_template, redirect, url_for, request
from flask_session import Session
import sqlite3


from password_generator import getStrongPassword


# salt = "salt"
with open('NationalBank/salt', 'r') as salt_file:
    salt = salt_file.read()

# dane do serwera Flask
template_dir = os.path.relpath('./templates')
app = Flask(__name__, template_folder=template_dir)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



def start_flask_server():
    app.run(host="127.0.0.1", port=5000, debug=True)

@app.route('/')
def index():
    return redirect(url_for("home"))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']     # c8b2505b76926abdc733523caa9f439142f66aa7293a7baaac0aed41a191eef6
        password = password + salt
        password = hashlib.sha256(password.encode()).hexdigest()

        # opening database connection
        db_conn = sqlite3.connect("database.db")
        db_cursor = db_conn.cursor()

        # check if the login exist
        query = f"SELECT login FROM credentials WHERE login='{username}'"
        is_login_valid = db_cursor.execute(query).fetchall()
        if(is_login_valid == []):
            error = "Invalid login!"
            return render_template('login.html', error=error)
        
        # password check
        query = f"SELECT password FROM credentials WHERE login='{username}'"
        is_password_valid = db_cursor.execute(query).fetchall()
        if(is_password_valid[0][0] != password):
            error = "Invalid password!"
            return render_template('login.html', error=error)

        # success!
        db_conn.close()
        return redirect(url_for('homepage', username=username))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == "POST":
        try:
            if request.form['get_strong_password'] is not None:
                return render_template('register.html', generated_password = getStrongPassword(20))
        except KeyError:
            pass

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        # opening database connection
        db_conn = sqlite3.connect("database.db")
        db_cursor = db_conn.cursor()

        # check is login avaliable
        query = f"SELECT login FROM credentials WHERE login='{username}'"
        is_login_aval = db_cursor.execute(query).fetchall()
        if(is_login_aval != []):
            error = "Login already in use!"
            return render_template('register.html', error=error)
        
        # email check
        email_check = re.findall('\S+@\S+\.\S+', email)
        if(email_check == []):
            error = "Invalid e-mail format!"
            return render_template('register.html', error=error)

        # TO DO

        # password check
        if len(password) < 12 or len(password) > 64:
            error = "Password must contains 12 to 64 letters!"
            return render_template('register.html', error=error)
        
        digits = re.search(r"\d", password)
        uppercase = re.search(r"[A-Z]", password)
        lowercase = re.search(r"[a-z]", password)
        symbols = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password)
        strength_check = all(element is not None for element in [digits, uppercase, lowercase, symbols])
        if(not strength_check):
            error = "Password must contain uppercase and lowercase letter, digit and symbol!"
            return render_template('register.html', error=error)

        # check are the password matching
        if(password != confirm_password):
            error = "Passwords are not matched!"
            return render_template('register.html', error=error)

    return render_template('register.html', error="Success!")

@app.route('/homepage')
def homepage():
    return(render_template('homepage.html', user=request.args.get('username')))

if(__name__ == "__main__"):
    start_flask_server()