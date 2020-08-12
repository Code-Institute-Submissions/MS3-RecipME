import os
# from bson.objectid import ObjectId
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

# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap

@app.route('/')
@app.route('/home')
def show_home():
    return render_template('index.html',
                           recipes=mongo.db.recipes.find())


@app.route('/recipe/<recipe_id>')
def show_recipe(recipe_id):
    # recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    recipe = mongo.db.recipes.find_one({'_id': recipe_id})
    return render_template('recipe.html', recipe=recipe)


# Sign up
@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()


@app.route('/user/signout')
def signout():
    return User().signout()


@app.route('/user/login', methods=['POST'])
def login():
    return User().login()


@app.route('/dashboard/')
@login_required
def dashboard():
    existing_user = mongo.db.users.find_one({'_id': session['username']})
    saved_recipes = mongo.db.recipes.find({'_id': {'$in': existing_user['recipes']}})
    return render_template('dashboard.html', saved_recipes=saved_recipes)


#login session testing
@app.route('/test')
def index():
    if 'username' in session:
        existing_user = mongo.db.users.find_one({'_id': session['username']})
        existing_recipes = jsonify(existing_user["recipes"])
        saved_recipes = mongo.db.recipes.find({'_id': {'$in': existing_user['recipes']}})
        # return 'You are logged in as ' + session['username']
        # return jsonify(session['user'])
        return existing_recipes

    return 'You are not logged in'

@app.route('/save_recipe/<recipe_id>')
def save_recipe(recipe_id):
    updated_recipes = []
    if session.get('username', None):
        username = session['username']
        user = mongo.db.users.find_one({'_id': username})
        # recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
        recipe = mongo.db.recipes.find_one({'_id': recipe_id})
        #  Update users recipes
        recipes = user['recipes']
        # if the recipe is not already in the list
        if recipe_id not in recipes:
            recipes.append(recipe_id)
            # recipes.append(ObjectId(recipe_id))

        mongo.db.users.update_one({'_id': user['_id']},
                            {"$set": {'recipes': recipes, }}, upsert=True)

        updated_user = mongo.db.users.find_one({'_id': username})
        updated_recipes = updated_user['recipes']

    return redirect(url_for('show_recipe', recipe_id=recipe_id, recipes=updated_recipes))


@app.route('/add_recipe/<user_id>')
def add_recipe(user_id):
    if session.get('USERNAME', None):
        username = session['USERNAME']
        # user exists in the database
        try:
            current_user = mongo.db.users.find_one({'username': username})
            requested_user = mongo.db.users.find_one({'_id': user_id})
            # if the current logged in user is the user requested
            if requested_user['_id'] == current_user['_id']:
                # Default recipe image
                # image_url = 'https://res.cloudinary.com/dajuujhvs/image/upload/v1591896759/gi5h7ejymbig1yybptcy.png'
                # image_url_id = 'gi5h7ejymbig1yybptcy'
                # create empty temp record
                temp_record = DB_RECIPES.insert_one(
                    {
                        'name': 'My Awesome Recipe',
                        'image_url': image_url,
                        'image_url_id': image_url_id,
                        'featured': 'false',
                        'current_rating': '0',
                        'total_ratings': 0,
                        'sum_ratings': 0,
                        'author_id': user_id,
                        'preptime_hrs': '0',
                        'preptime_min': '0',
                        'cooktime_hrs': '0',
                        'cooktime_min': '0'
                    })
                return redirect(url_for('edit_recipe', user_id=user_id, recipe_id=temp_record.inserted_id))
            else:
                # raises a 403 error
                return abort(403, description="Forbidden")
        except:
            # raises a 404
            return abort(404, description="Resource not found")
    else:
        # User not signed in
        return redirect(url_for('sign_in'))


class User:

    def start_session(self, user): 
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        session['username'] = session['user']['_id']
        return jsonify(user), 200

    def signup(self):

        # debugging

        print(request.form)

        # Create user object

        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
            "recipes": []
        }

        # encrypt
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        if mongo.db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email address already in use"}), 400

        # recipe_insert = {"_id":uuid.uuid4().hex,"recipe_name":"cereal 8","recipe_description":"simple morning meal","recipe_ingredients":["cornflakes","milk","sugar"],"prep_time":"5 min","cook_time":"0 min","serves":"1","recipe_steps":["get bowl","add cornflakes","add milk","add sugar"],"notes":"not too much sugar","img_url":"https://res.cloudinary.com/dm2vu1yzr/image/upload/v1596794708/Cornflakes_in_bowl_vmnm7z.jpg","difficulty":"easy"}
        # mongo.db.recipes.insert_one(recipe_insert)

        # add user to DB
        if mongo.db.users.insert_one(user):
            return self.start_session(user)

        return jsonify({"error": "Signup failed"}), 400

    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):

        user = mongo.db.users.find_one({"email": request.form.get('email')})

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        return jsonify({"error": "Invalid login credentials"}), 401


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
