import os
# from bson.objectid import ObjectId
from flask import Flask, render_template, redirect, request, url_for, jsonify, session
from flask_pymongo import PyMongo
from passlib.hash import pbkdf2_sha256
from functools import wraps
from cloudinary.uploader import upload, destroy
import cloudinary as Cloud
import uuid

# Local deploy only
from os import path
if path.exists("env.py"):
    import env
    from env import secret_key, db_name


app = Flask(__name__)
app.config["MONGO_DBNAME"] = db_name
app.config["MONGO_URI"] = os.getenv('MONGO_URI')
Cloud.config.update = ({
    'cloud_name':os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.environ.get('CLOUDINARY_API_KEY'),
    'api_secret': os.environ.get('CLOUDINARY_API_SECRET')
})


# app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost') #Heroku Deployment


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
    recipe = mongo.db.recipes.find_one({'_id': recipe_id})
    owner = mongo.db.users.find_one({'_id': recipe['owner']})
    if session.get('username', None):
        # recipe = mongo.db.recipes.find_one({'_id': recipe_id})
        # owner = mongo.db.users.find_one({'_id': recipe['owner']})
        existing_user = mongo.db.users.find_one({'_id': session['username']})
        return render_template('recipe.html', recipe=recipe, recipe_id=recipe_id, owner=owner, active_user=existing_user)

    return render_template('recipe.html', recipe=recipe, recipe_id=recipe_id,owner=owner)



# Sign up
@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()


@app.route('/recipe/add', methods=['POST'])
def add_recipe():
    return Recipe().add()


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
    saved_recipes = mongo.db.recipes.find(
        {'_id': {'$in': existing_user['recipes']}})
    return render_template('dashboard.html', active_user=existing_user, saved_recipes=saved_recipes)


# testing //////////////////////////////////////////////////////////////
@app.route('/add_image/<recipe_id>',methods=['GET', 'POST'])
def add_image(recipe_id):
    ufile = request.files.get('file')
    print(ufile)
    if ufile:
        print("File Found")
        uploaded = upload(ufile)
        image_url = uploaded['secure_url']
        print(image_url)
        mongo.db.recipes.update_one({'_id': recipe_id}, {"$set": {
            'img_url': image_url,
        }}, upsert=True)
    else:
        print('no file found')
    return redirect(url_for('show_recipe', recipe_id=recipe_id))



# ///////////////////////////////////////////////////////////////////

@app.route('/save_recipe/<recipe_id>')
def save_recipe(recipe_id):
    updated_recipes = []
    if session.get('username', None):
        username = session['username']
        user = mongo.db.users.find_one({'_id': username})
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

@app.route('/remove_recipe/<recipe_id>')
def remove_recipe(recipe_id):
    updated_recipes = []
    if session.get('username', None):
        username = session['username']
        user = mongo.db.users.find_one({'_id': username})
        recipe = mongo.db.recipes.find_one({'_id': recipe_id})
        #  Update users recipes
        recipes = user['recipes']
        # if the recipe is not already in the list
        if recipe_id in recipes:
            recipes.remove(recipe_id)
            # recipes.append(ObjectId(recipe_id))

        mongo.db.users.update_one({'_id': user['_id']},
                                  {"$set": {'recipes': recipes, }}, upsert=True)

        updated_user = mongo.db.users.find_one({'_id': username})
        updated_recipes = updated_user['recipes']

    return redirect(url_for('show_recipe', recipe_id=recipe_id, recipes=updated_recipes))

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    username = session['username']
    recipe = mongo.db.recipes.find_one({'_id': recipe_id})
    owner = mongo.db.users.find_one({'_id': recipe['owner']})
    existing_user = mongo.db.users.find_one({'_id': session['username']})
    user = mongo.db.users.find_one({'_id': username})
    if session.get('username', None):
        return render_template('edit-recipe.html', recipe=recipe, recipe_id=recipe_id, owner=owner, active_user=existing_user)

    return render_template('recipe.html', recipe=recipe, recipe_id=recipe_id,owner=owner)




@app.route('/edit_recipe/<recipe_id>',methods=['GET', 'POST'])
def update_recipe(recipe_id):
    username = session['username']
    recipe = mongo.db.recipes.find_one({'_id': recipe_id})
    owner = mongo.db.users.find_one({'_id': recipe['owner']})
    existing_user = mongo.db.users.find_one({'_id': session['username']})
    user = mongo.db.users.find_one({'_id': username})
    if session.get('username', None):
        recipe_ingredients = []

        for x in range(1, 41):
            if request.form.get("edit-ingredient-%d" % (x)):
                recipe_ingredients.append(request.form.get("edit-ingredient-%d" % (x)))

        recipe_steps = []

        for x in range(1, 41):
            if request.form.get("edit-step-%d" % (x)):
                recipe_steps.append(request.form.get("edit-step-%d" % (x)))

        mongo.db.recipes.update_one({'_id': recipe_id}, {"$set": {
            'recipe_name': request.form.get('edit-recipient-name'),
            'recipe_description': request.form.get('edit-recipe-description'),
            "recipe_ingredients": recipe_ingredients,
            "recipe_steps": recipe_steps,
            'notes': request.form.get('edit-recipe-notes'),
            'prep_time': request.form.get('edit-prep-time'),
            'cook_time': request.form.get('edit-cook-time'),
            'serves': request.form.get('edit-serves'),
            "difficulty": request.form.get('edit-difficulty'),
            'owner': user['_id'],
        }}, upsert=True)

        return redirect(url_for('show_recipe', recipe_id=recipe_id))

    return render_template('recipe.html', recipe=recipe, recipe_id=recipe_id,owner=owner)




# ////////////////////////////////////////////////////////////////////////////
class Recipe:


    def add(self):

        recipe_ingredients = []

        for x in range(1, 41):
            if request.form.get("ingredient-%d" % (x)):
                recipe_ingredients.append(request.form.get("ingredient-%d" % (x)))

        recipe_steps = []

        for x in range(1, 41):
            if request.form.get("step-%d" % (x)):
                recipe_steps.append(request.form.get("step-%d" % (x)))

        recipe_insert = {
            "_id": uuid.uuid4().hex,
            "recipe_name": request.form.get('recipient-name'),
            "recipe_description": request.form.get('recipe-description'),
            "recipe_ingredients": recipe_ingredients,
            "prep_time": request.form.get('prep-time'),
            "cook_time": request.form.get('cook-time'),
            "serves": request.form.get('serves'),
            "recipe_steps": recipe_steps,
            "notes": request.form.get('recipe-notes'),
            "img_url": 'https://res.cloudinary.com/dm2vu1yzr/image/upload/v1597575587/ynfzhoovai1r2jkjjq4l.png',
            "difficulty": request.form.get('difficulty'),
            "owner": session['username']
        }

        # recipe_insert = list(filter(None, data))

        if mongo.db.recipes.insert_one(recipe_insert):
            return jsonify(recipe_insert), 200

        return jsonify({"error": "Add Failed"}), 400

# ////////////////////////////////////////////////////////////////////////////


class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        session['username'] = session['user']['_id']
        return jsonify(user), 200

    def signup(self):

        # debugging

        # print(request.form)

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
