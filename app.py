from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exception import Unauthorized

from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def homepage():
    '''Go to homepage'''

    return redirect('/register')

@app.route('/register', methods = ['GET', 'POST'])
    '''Produce form and handle its submission'''

    if 'username' in session:
        return redirect(f'/users/{session['username']}')

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data 

        user = User.register(username, password, first_name, last_name, email)]

        db.session.commit()
        session['username'] = user.username

        return redirect(f'/users/{user.username}')

    else:
        return render_template('user/register.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    '''Produce form and handle login'''

    if 'username' in session:
        return redirect(f'/users/{session['username']}')

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user: 
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.error = ['Invalid username or password.']
            return render_template('users/login.html', form = form)

    return render_template('users/login.html', form = form)

@app.route('/logout')
def logout():
    '''Route for logout'''

    session.pop('username')
    return redirect('/login')

@app.route('/users<username>/feedback/new', methods = ['GET', 'POST'])
def new_feedback(username):
    '''Show feedback and process it'''

    if 'username' not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title = title,
            content = content,
            username = username
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f'/users/{feedback.username}')

    else:
        return render_template('feedback/new.html', form = form)

@app.route('/feedback/<int:feedback_id>/update', methods = ['GET', 'POST'])
def update_feedback(feedback_id):
    '''Show updated feedback'''

    feedback = Feedback.query.get(feedback_id)

    if 'username' not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj = feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f'/users/{feedback.username}')

    return render_template('/feedback/edit.html', form = form, feedback = feedback = feedback)

@app.route('/feedback/<int:feedback_id/delete>', methods = ['POST'])
def delete_feedback(feedback_id):
    '''Deletes feedback from db'''

    feedback = Feedback.query.get(feedback_id)
    if 'username' not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f'/users/{feedback.username}')