import os

from flask import Flask
from flask import session
from flask import redirect
from flask import url_for
from flask import flash
from flask import render_template
from flask_script import Manager

from flask_wtf import Form
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import Required

from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'vLIiT3Qcht68WF8NakLeeGOGLuGgluuGdEVK6psOXsDdO3u3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
manager = Manager(app)
db = SQLAlchemy(app)

# ---------- ORM -----------
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # 为了实现更精确的查询，加入lazy参数 ？？？
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

class NameForm(Form):
    name = StringField('What\'s your name?', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
          user = User(username=form.name.data)
          db.session.add(user)
          session['know'] = False
        else:
          session['know'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), know=session.get('know', False))

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
