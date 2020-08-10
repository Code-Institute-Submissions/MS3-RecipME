import os
from bson.objectid import ObjectId
from flask import Flask, render_template, redirect, request, url_for, jsonify, session
from flask_pymongo import PyMongo
from passlib.hash import pbkdf2_sha256
from functools import wraps
import uuid

# Local deploy only
from os import path
if path.exists("env.py"):
    import env
    from env import secret_key


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'cookbook'
app.config["MONGO_URI"] = os.getenv('MONGO_URI')
# app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost') #Heroku Deplyment


mongo = PyMongo(app)
app = Flask(__name__)
app.secret_key = secret_key


@app.route('/')
@app.route('/home')
def show_home():
    return render_template('index.html',
                           recipes=mongo.db.recipes.find())


@app.route('/recipe/<recipe_id>')
def show_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('recipe.html', recipe=recipe)


# Sign up
@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()


@app.route('/user/signout')
def signout():
    return User().signout()


class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):

        # debugging

        print(request.form)

        # Create user object

        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }

        # encrypt
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        if mongo.db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email address already in use"}), 400

        # add user to DB
        if mongo.db.users.insert_one(user):
            return self.start_session(user)
            # return jsonify(user), 200

        return jsonify({"error": "Signup failed"}), 400

    def signout(self):
        session.clear()
        return redirect('/')


# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap


@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
