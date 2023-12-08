from flask import Flask, render_template, flash, redirect, url_for
from flask import g, session
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, CommunityForm, MessageForm, LoginForm, PostForm, JoinForm, EditProfileForm
from models import Community, User, Message, Post

from __init__ import app, db

app.secret_key = 'cool'

@app.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id is not None:
        g.user = User.query.get(user_id)
    else:
        g.user = None

@app.route('/')
def home():
    communities = Community.query.all()
    return render_template('home.html', communities=communities)

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
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered.', 'danger')
        else:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "user_id" in session:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        print (form.username.data)
        print (form.password.data)
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session["username"] = user.username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            if user is None:
                flash('Username not found', 'danger')
            else:
                flash('Invalid password', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/create_community', methods=['GET', 'POST'])
def create_community():
    if 'user_id' not in session:
        flash('You must be logged in to create a community.', 'danger')
        return redirect(url_for('login'))

    form = CommunityForm()
    if form.validate_on_submit():
        user = User.query.get(session['user_id'])  # Get the current user
        if user is None:
            flash('User not found.', 'danger')
            return redirect(url_for('home'))

        new_community = Community(name=form.name.data, description=form.description.data)
        new_community.members.append(user)  # Add the user as a member
        db.session.add(new_community)
        db.session.commit()
        flash('Your community has been created and you are now a member!', 'success')
        return redirect(url_for('community', community_id=new_community.id))

    return render_template('create_community.html', form=form)




@app.route('/communities')
def communities():
    all_communities = Community.query.all()
    return render_template('communities.html', communities=all_communities)

@app.route('/community/<int:community_id>')
def community(community_id):
    community = Community.query.get_or_404(community_id)
    posts = Post.query.filter_by(community_id=community.id).all()
    post_form = PostForm()
    join_form = JoinForm()  # Make sure you have imported this form at the top
    user_is_member = False
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        user_is_member = user in community.members  # This checks if the user object is in the members list
    return render_template('community.html', community=community, posts=posts, post_form=post_form, join_form=join_form, user_is_member=user_is_member)


@app.route('/community/<int:community_id>/join', methods=['POST'])
def join_community(community_id):
    # Ensure the user is logged in
    if 'user_id' not in session:
        flash('You must be logged in to join a community.', 'danger')
        return redirect(url_for('login'))

    # Fetch the user and community instances
    user = User.query.get(session['user_id'])
    community = Community.query.get_or_404(community_id)

    # Check if the user instance is valid
    if user is None:
        flash('User not found.', 'danger')
        return redirect(url_for('home'))

    # Check if the user is already a member
    if user in community.members:
        flash('You are already a member of this community.', 'info')
    else:
        # Add the user to the community members and commit the session
        community.members.append(user)
        db.session.commit()
        flash('You have joined the community!', 'success')

    return redirect(url_for('community', community_id=community_id))


@app.route('/community/<int:community_id>/create_post', methods=['GET', 'POST'])
def create_post(community_id):
    if 'user_id' not in session:
        flash('You need to be logged in to create a post.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    community = Community.query.get(community_id)
    
    # Check if the user is a member of the community
    if community is None or user not in community.members:
        flash('You must join the community to post here.', 'warning')
        return redirect(url_for('community', community_id=community_id))

    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data, 
            content=form.content.data, 
            community_id=community_id,
            author_id=user.id  # Use the id of the user fetched from the session
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('community', community_id=community_id))

    return render_template('create_post.html', form=form, community_id=community_id)



@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if not "user_id" in session:
        return redirect(url_for('login'))

    form = MessageForm()
    if form.validate_on_submit():
        message = Message(username=session["username"], text=form.message.data)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('chat'))
    messages = Message.query.order_by(Message.timestamp.asc()).all()
    return render_template('chat.html', form=form, messages=messages)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
@app.route('/profile', methods=["GET"])
def profile():
    if 'user_id' not in session:
        flash('You must be logged in to view this page.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get_or_404(session['user_id'])
    user_communities = Community.query.filter(Community.members.any(id=user.id)).all()
    user_posts = Post.query.filter_by(author_id=user.id).all()
    return render_template('profile.html', user=user, communities=user_communities, posts=user_posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        flash('You must be logged in to view this page.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get_or_404(session['user_id'])
    form = EditProfileForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.bio = form.bio.data
        user.location = form.location.data
        # Save other fields as necessary
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', form=form)