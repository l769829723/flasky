from flask import Flask
from flask import render_template
from flask_script import Manager

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'vLIiT3Qcht68WF8NakLeeGOGLuGgluuGdEVK6psOXsDdO3u3'
manager = Manager(app) 

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/user/<name>/')
def user(name):
  return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
  return render_template('500.html'), 500

if __name__ == '__main__':
  manager.run()
