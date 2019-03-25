from flask import render_template, redirect, request, session, flash
from config import bcrypt
from models import likes_table, follows_table, User, Tweet

def index():
    if 'userid' in session:
        return redirect('/dashboard')
    return render_template('index.html')

def process():
    validation = User.validate(request.form)
    if validation:
        return redirect('/')

    new_user = User.adduser(request.form)
    session['userid'] = new_user.id

    return redirect('/')

def login():
    user = User.query.filter_by(email=request.form['email']).first()

    if user and bcrypt.check_password_hash(user.pw_hash, request.form['password']):
        session['userid'] = user.id
        return redirect('/')
    
    flash('invalid email or password', 'login')
    return redirect('/')

def active():
    if not 'userid' in session:
        return redirect('/')

    user = User.query.get(session['userid'])
    all_tweets = Tweet.query.filter(Tweet.user_id.in_([each.id for each in user.followed])).order_by(Tweet.created_at.desc()).all()
    return render_template('welcome.html', user = user.first_name, all_tweets = all_tweets)

def logout():
    if 'userid' in session:
        session.pop('userid')
    return redirect('/')

def create_tweet():
    if not 'userid' in session:
        return redirect('/')
    if Tweet.validate_tweet(request.form):
        return redirect('/dashboard')
    else:
        Tweet.add_tweet(request.form)
        return redirect('/dashboard')

def add_like(id):
    Tweet.like(id)
    return redirect('/dashboard')

def delete_tweet(id):
    Tweet.remove_tweet(id)
    return redirect('/dashboard')

def edit_tweet(id):
    if not 'userid' in session:
        return redirect('/')
    id_test = Tweet.query.get(id)
    if session['userid'] == id_test.user_id:
        tweet = id_test
        return render_template('edit.html', tweet_id = id, tweet = tweet.content)
    return redirect('/')

def update_tweet(id):
    if Tweet.validate_tweet(request.form):
        return redirect('/tweets/{}/edit'.format(id))
    Tweet.change_tweet(request.form, id)
    return redirect('/dashboard')

def show_user_list():
    if not 'userid' in session:
        return redirect('/')
    all_users = User.query.all()
    return render_template('users.html', all_users = all_users)

def follow_user(id):
    User.follow(id)
    return redirect('/users')

def check_email():
    found = False
    email = User.query.filter_by(email=request.form['email']).first()
    print('key_lift')
    if email:
        found = True
    return render_template('partials/email.html', found=found)