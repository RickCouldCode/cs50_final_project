from flask import Flask, render_template, flash, redirect, url_for
from flask import session
from flask import g
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm
from forms import CommunityForm
from forms import MessageForm
from models import Community
from models import User, Message
from forms import LoginForm

from __init__ import app,db


app.secret_key = 'cool'

# @app.before_request
# def load_logged_in_user():
    
#     user_id = session['user_id']
#     if user_id is None:
#         print('1')
#         g.user = None
#     else:
#         print('2')
#         g.user = User.query.get(user_id)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/gardens')
def gardens():
    return render_template('gardens.html')

@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if "user_id" in session:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        print()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if "user_id" in session and session["user_id"]:
        return redirect(url_for('home'))

    form = LoginForm()
    print("here in login")
    if form.validate_on_submit():
        print("login form validated")
        # print(f"Username: {}")
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        # RICK TODO make user_id not always 2
        session['user_id'] = 2
        session["username"] = form.username.data
        User.id
        # print('3')
        # g.user = 2
        flash('Logged in successfully!', 'success')
        return redirect(url_for('home'))
        # else:
        #     flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)


        # user = User.query.filter_by(username=form.username.data).first()
        # if user and user.check_password(form.password.data):

@app.route('/create_community', methods=['GET', 'POST'])
def create_community():
    if not g.user:  # Redirect to login if user is not logged in
        return redirect(url_for('login'))

    form = CommunityForm()  # Using the CommunityForm from forms.py
    if form.validate_on_submit():
        # Creating a new community instance
        new_community = Community(name=form.name.data, description=form.description.data)
        db.session.add(new_community)
        db.session.commit()  # Saving the community to the database
        return redirect(url_for('community', id=new_community.id))  # Redirect to the newly created community page

    return render_template('create_community.html', form=form)  # Render the community creation form

@app.route('/community/<int:community_id>/create_post', methods=['GET', 'POST'])
def create_post(community_id):
    if not g.user:
        return redirect(url_for('login'))  # Redirect if not logged in

    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, community_id=community_id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('community', community_id=community_id))  # Redirect to the community page
    return render_template('create_post.html', form=form)

@app.route('/communities')
def communities():
    all_communities = Community.query.all()
    return render_template('communities.html', communities=all_communities)

@app.route('/community/<int:community_id>')
def community(community_id):
    community = Community.query.get_or_404(community_id)
    posts = Post.query.filter_by(community_id=community.id).all()
    return render_template('community.html', community=community, posts=posts)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if not session["user_id"]:
        print('no session user id')
        return redirect(url_for('login'))

    form = MessageForm()
    if form.validate_on_submit():
        message = Message(username=session["username"] if "username" in session else "ERROR", text=form.message.data)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('chat'))
    messages = Message.query.order_by(Message.timestamp.asc()).all()
    return render_template('chat.html', form=form, messages=messages)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
