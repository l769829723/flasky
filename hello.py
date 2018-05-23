from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)

@app.route('/')
def index():
  # response = make_response('<h1>This document carries a cookie!</h1>')
  # user_agent = request.headers.get('User-Agent')
  # response.set_cookie('answer', '42')
  return redirect('https://www.baidu.com')

@app.route('/user/<name>/')
def user(name):
  return '<h1>Hello, {}!</h1>'.format(name)

if __name__ == '__main__':
  manager.run()
