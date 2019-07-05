from flask import Flask, request
app = Flask(__name__)

@app.route('/login')
def login():
    username = request.form['user']
    password = request.form['pass']
    print(username)
    print(password)

if __name__ == '__init__':
    app.run()