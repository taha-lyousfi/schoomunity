# Purpose: Create a Flask app and define the necessary API routes

from flask import Flask, jsonify, request, abort, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from models import (User, Post)
import os

from models import db


port = int(os.environ.get('PORT', 5000))

# Initialize Flask app with SQLAlchemy
app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
SECRET_KEY = "tech_with_taha_12345_random_k#{okd"


@app.route('/')
def main_page():
    return '<html><head><title>During Development</title></head><body>A RESTful API in Flask using SQLAlchemy. For our <a href="https://www.schoomunity.cf" target="_blank">School Community</a> Website.</body></html>'


@app.route('/api/login', methods=['POST'])
def login():
    # try:
    user_ = User.query.filter_by(
        username=request.form['username']).first()
    if user_.check_hash(request.form['password']):
        return jsonify({'user': user_.serializeable}), 200
    else:
        print('else!')
        return "Wrong Credentials!"
    # except:
    #     return "Wrong Credentials! in except"


@app.route('/api/users/<username>')
def show_user(username):
    try:
        user = User.query.filter_by(username=username).first()
        return jsonify(user.serialize)
    except:
        return not_found("User does not exist")


@app.route('/api/users', methods=['POST'])
def create_user():
    print(request.form['username'])
    try:
        user = User(request.form)
        db.session.add(user)
        db.session.commit()
        return jsonify({'user': user.serialize}), 201
    except KeyError:
        return bad_request('Missing required data.')
    except:
        return bad_request("An error occured !!")


@app.route('/api/users/edit', methods=['POST'])
def edit_user():
    print(request.form['old_username'])
    try:
        user = User.query.filter_by(
            username=request.form['old_username']).first_or_404()
        if user.check_hash(request.form['old_password']):
            user.update(request.form)
        else:
            return bad_request('Incorrect password')
        return jsonify({'user': user.serialize}), 201
    except KeyError:
        return bad_request('Missing required data.')
    except:
        return bad_request('Something went wrong!')


@app.route('/api/posts/<id>')
def show_post(id):
    try:
        post = Post.query.filter_by(id=id).first_or_404()
        return jsonify({'post': post.serialize,
                        'user': post.user})
    except:
        return not_found("Post does not exist.")


@app.route('/api/posts', methods=['POST'])
def create_post():
    request_json = request.form
    try:
        if 'username' in request_json and 'password' in request_json:
            try:
                if User.query.filter_by(username=request_json['username']).first().check_hash(request_json['password']):
                    post = Post(request_json)
                    db.session.add(post)
                    db.session.commit()
                    return jsonify({'post': post.serialize}), 201
                else:
                    # return redirect('https://schoomunity.cf/#/login')
                    return bad_request('Else statement')
            except KeyError:
                # return redirect('https://schoomunity.cf/#/login')
                return bad_request('KeyError!!')
        else:
            return bad_request('Missing required data.')
    except KeyError:
        return bad_request('Missing required data.')
    except:
        return bad_request('Given user_id does not exist or there is an error in the credentials.')


@app.route('/api/posts/edit', methods=['POST'])
def edit_post():
    try:
        user = User.query.filter_by(
            username=request.form['username']).first_or_404()
        if user.check_hash(request.form['password']):
            post = Post.query.filter_by(id=request.form["id"])
            if post.user_id == request.form['user_id']:
                post.update(request.form)
            else:
                return bad_request("You don't have the permission to edit this post!!")
        else:
            return bad_request('Incorrect password')
        return jsonify({'post': post.serialize}), 201
    except KeyError:
        return bad_request('Missing required data.')
    except:
        return bad_request('Something went wrong!')


# Custom Error Helper Functions
def bad_request(message):
    response = jsonify({'error': message})
    response.status_code = 400
    return response


def not_found(message):
    response = jsonify({'error': message})
    response.status_code = 404
    return response


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=port, debug=True)
