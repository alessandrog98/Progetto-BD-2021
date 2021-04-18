from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/users')
def users():
    return 'if u are a registerd user, please insert the username here: '

@app.route('/login', methods=['GET', 'POST'])
def login():
    user = request.form["user"]
    return redirect(url_for('show_profile', username=user))

@app.route('/users/<username>')
def show_profile(username):
    users = ['alice','bob','charlie']
    if username in users:
        return render_template('profile.html', user=username)
    else:
        return render_template('profile.html', reg=users)

