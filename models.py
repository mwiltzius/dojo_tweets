from flask import flash, session
from config import db, bcrypt, EMAIL_REGEX, PASS_REGEX
from sqlalchemy.sql import func

likes_table = db.Table('likes',
              db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
              db.Column('tweet_id', db.Integer, db.ForeignKey('tweet.id', ondelete='cascade'), primary_key=True),
              db.Column('created_at', db.DateTime, server_default=func.now()),
              db.Column('updated_at', db.DateTime, server_default=func.now(), onupdate=func.now())
              )

follows_table = db.Table('follows',
                db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                db.Column('created_at', db.DateTime, server_default=func.now()),
                db.Column('updated_at', db.DateTime, server_default=func.now(), onupdate=func.now())
                )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    pw_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    tweets_liked = db.relationship('Tweet', secondary=likes_table, cascade='all')
    followers = db.relationship('User',
        secondary=follows_table,
        primaryjoin=id==follows_table.c.followed_id,
        secondaryjoin=id==follows_table.c.follower_id,
        backref='followed',
        cascade='all'
        )
    
    @classmethod
    def validate(cls, data):
        errors = []
        user_test = cls.query.filter_by(email=data['email']).first()
        if user_test:
            errors.append('Email already in use')

        if len(data['fname']) < 1:
            errors.append('First Name left blank')
        elif not data['fname'].isalpha():
            errors.append('First Name can only contain letters')
        if len(data['lname']) < 1:
            errors.append('Last Name left blank')
        elif not data['lname'].isalpha():
            errors.append('Last Name can only contain letters')
        if len(data['email']) < 1:
            errors.append('Email left blank')
        elif not EMAIL_REGEX.match(data['email']):
            errors.append('Email must be valid')
        if not PASS_REGEX.match(data['password']):
            errors.append('Password must be at least 5 characters, and contain at least one letter and number')
        if not data['password'] == data['pass_conf']:
            errors.append('Passwords do not match')

        if errors:
            for each_error in errors:
                flash(each_error, 'register')
            return True
        else:
            return False
        
    @classmethod
    def adduser(cls, data):
        pw_hash = bcrypt.generate_password_hash(data['password'])
        new_user = cls(first_name=data['fname'], last_name=data['lname'], email=data['email'], pw_hash=pw_hash)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def follow(cls, id):
        follower = cls.query.get(session['userid'])
        followed = cls.query.get(id)
        followed.followers.append(follower)
        db.session.commit()

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref("tweets", cascade="all, delete-orphan"))
    user_likes = db.relationship('User', secondary=likes_table)

    @classmethod
    def validate_tweet(cls, data):
        tweet_error = []
        print(data['tweet'])
        if len(data['tweet']) < 1:
            tweet_error.append('tweeting field is blank')
        if len(data['tweet']) > 255:
            tweet_error.append('tweets must be less than 255 characters')
        if tweet_error:
            flash(tweet_error[0])
            return True
        else:
            return False

    @classmethod
    def add_tweet(cls, data):
        tweet = cls(content=data['tweet'], user_id=session['userid'])
        db.session.add(tweet)
        db.session.commit()
        return tweet

    @classmethod
    def change_tweet(cls, data, id):
        tweet = cls.query.get(id)
        tweet.content = data['tweet']
        db.session.commit()

    @classmethod
    def remove_tweet(cls, id):
        id_test = cls.query.get(id)
        if session['userid'] == id_test.user_id:
            db.session.delete(id_test)
            db.session.commit()
        return id_test

    @classmethod
    def like(cls, id):
        user = User.query.get(session['userid'])
        tweet = cls.query.get(id)
        tweet.user_likes.append(user)
        db.session.commit()
        return tweet