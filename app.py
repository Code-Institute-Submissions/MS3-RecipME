import os
from flask import Flask, render_template, redirect, request, url_for, jsonify, session
from flask_pymongo import PyMongo, pymongo
from passlib.hash import pbkdf2_sha256
from functools import wraps
from cloudinary.uploader import upload, destroy
import cloudinary as Cloud
import uuid
import json

# Local deploy 
from os import path
if path.exists("env.py"):
    import env
    from env import secret_key, db_name


app = Flask(__name__)
# app.config["MONGO_DBNAME"] = db_name
# app.config["MONGO_URI"] = os.getenv('MONGO_URI')
Cloud.config.update = ({
    'cloud_name':os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.environ.get('CLOUDINARY_API_KEY'),
    'api_secret': os.environ.get('CLOUDINARY_API_SECRET')
})
 #Heroku Deployment
app.config["MONGO_DBNAME"] = os.getenv('db_name', 'mongodb://localhost')
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')
# app.secret_key = os.getenv('secret_key')



mongo = PyMongo(app)
app = Flask(__name__)
# app.secret_key = secret_key
app.secret_key = os.getenv('secret_key')


def login_required(f):
    # redirect to control access to functions that require logged in user
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
    #homepage function that displays featured recipes (based on highest rating & rating count) and the top user & top users recipe (by high rating)
    recipes = mongo.db.recipes.find()

    feature_coll = top_recipe_coll = mongo.db.recipes.find().sort([('avg_rating', -1), ('count_rating', -1)]).limit(3)
    try:
        # display top rated user and that users top rated recipe
        top_user_coll = mongo.db.users.find().sort([('avg_rating', -1), ('count_rating', -1)]).limit(1)
        top_user=top_user_coll[0]

        top_recipe_coll = mongo.db.recipes.find({'owner':top_user['_id']}).sort([('avg_rating', -1), ('count_rating', -1)]).limit(1)
        top_recipe=top_recipe_coll[0]
    except:
        return render_template('index.html', recipes=recipes, feature_coll=feature_coll)


    return render_template('index.html', recipes=recipes,top_user=top_user, top_recipe=top_recipe, feature_coll=feature_coll)


@app.route('/recipe/<recipe_id>')
def show_recipe(recipe_id): 
    #used to display all the essentail detail of a given recipe upon navigating to that recipe
    recipe = mongo.db.recipes.find_one({'_id': recipe_id})
    owner = mongo.db.users.find_one({'_id': recipe['owner']})
    rating_msg = request.args.get('rating_msg')
    try:
        active_user = mongo.db.users.find_one({'_id': session['username']})
    except:
        active_user = ""

    return render_template('recipe.html', recipe=recipe, recipe_id=recipe_id, owner=owner, active_user=active_user, rating_msg=rating_msg)

@app.route('/user/<user_id>')
def user_recipes(user_id): 
    #displays all recipes owned/authored by a specific user
    recipes = mongo.db.recipes.find()
    user = mongo.db.users.find_one({'_id': user_id})
    #if recipes for user is active user bring to dashboard, else to dedicated page of other user recipes
    if session.get('username', None):
        if user_id == session['username']:
            return redirect(url_for('dashboard'))
        else:
            return render_template('user-recipes.html', user=user, recipes=recipes)
    else:
        return render_template('user-recipes.html', user=user, recipes=recipes)


@app.route('/user/signup', methods=['POST'])
def signup(): 
    #Call signup function from user class
    return User().signup()


@app.route('/recipe/add', methods=['POST'])
@login_required
def add_recipe(): 
    #Call add function from recipe class
    return Recipe().add()


@app.route('/user/signout')
def signout(): 
    #Call signout function from user class
    return User().signout()


@app.route('/user/login', methods=['POST'])
def login(): #Call login function from user class
    return User().login()


@app.route('/dashboard/',methods=['GET', 'POST'])
@login_required
def dashboard():
     #displays all detail in relation to the current logged in session user to own dashboard that shows their authord and saved recipes and basic chart data to their authored recipes rating breakdown and most counted
    active_user = mongo.db.users.find_one({'_id': session['username']})
    saved_recipes = mongo.db.recipes.find({'_id': {'$in': active_user['recipes']}})
    owned_recipes = mongo.db.recipes.find({'owner': active_user['_id']})
    top_recipe_coll = mongo.db.recipes.find({'owner': active_user['_id']}).sort([('avg_rating', -1), ('count_rating', -1)]).limit(5)

    try:
    #if avialable return information used in population of dashboard graphs
        recipe_names = []
        recipe_rating_count = []
        for top_recipe in top_recipe_coll:
            recipe_names.append(top_recipe['recipe_name'])
            recipe_rating_count.append(top_recipe['count_rating'])

        rating_coll = []

        one_star_ratings = []
        two_star_ratings = []
        three_star_ratings = []
        four_star_ratings = []
        five_star_ratings = []

        one_stars = mongo.db.ratings.find({'owner_id': active_user['_id'],'rating': "1"})
        for one_star in one_stars:
            one_star_ratings.append(one_star['rating'])
        one_star_count = len(one_star_ratings)
        rating_coll.append(one_star_count)

        two_stars = mongo.db.ratings.find({'owner_id': active_user['_id'],'rating': "2"})
        for two_star in two_stars:
            two_star_ratings.append(two_star['rating'])
        two_star_count = len(two_star_ratings)
        rating_coll.append(two_star_count)

        three_stars = mongo.db.ratings.find({'owner_id': active_user['_id'],'rating': "3"})
        for three_star in three_stars:
            three_star_ratings.append(three_star['rating'])
        three_star_count = len(three_star_ratings)
        rating_coll.append(three_star_count)

        four_stars = mongo.db.ratings.find({'owner_id': active_user['_id'],'rating': "4"})
        for four_star in four_stars:
            four_star_ratings.append(four_star['rating'])
        four_star_count = len(four_star_ratings)
        rating_coll.append(four_star_count)

        five_stars = mongo.db.ratings.find({'owner_id': active_user['_id'],'rating': "5"})
        for five_star in five_stars:
            five_star_ratings.append(five_star['rating'])
        five_star_count = len(five_star_ratings)
        rating_coll.append(five_star_count)
    except:
        return render_template('dashboard.html', active_user=active_user, saved_recipes=saved_recipes, owned_recipes=owned_recipes)

    return render_template('dashboard.html', active_user=active_user, saved_recipes=saved_recipes, owned_recipes=owned_recipes, rating_coll=rating_coll, recipe_names=recipe_names, recipe_rating_count=recipe_rating_count)


@app.route('/add_image/<recipe_id>',methods=['GET', 'POST'])
@login_required
def add_image(recipe_id): 
    #Validated @login covers non signed in users / validate_owner() prevents non owner from uploading new image
    if validate_owner(recipe_id) == True:
        ufile = request.files.get('file')
        # validate there is a file to upload
        if ufile:
            recipe = mongo.db.recipes.find_one({'_id': recipe_id})
            try:
                #if there is existing image delete from cloudinary
                destroy(recipe['image_public_id'], invalidate=True)
            except:
                pass
            #upload new image to cloudinary and add the associated information to the recipe in DB
            uploaded = upload(ufile)
            image_url = uploaded['secure_url']
            public_id = uploaded['public_id']

            mongo.db.recipes.update_one({'_id': recipe_id}, {"$set": {
                'img_url': image_url,
                'image_public_id': public_id,
            }}, upsert=True)
        else:
            pass
        return redirect(url_for('show_recipe', recipe_id=recipe_id))
    else:
        return redirect(url_for('show_recipe', recipe_id=recipe_id))

@app.route('/save_recipe/<recipe_id>')
@login_required
def save_recipe(recipe_id): 
    #function to save other user recipes to your collection for easy access 
    updated_recipes = []
    if session.get('username', None):
        username = session['username']
        user = mongo.db.users.find_one({'_id': username})
        recipe = mongo.db.recipes.find_one({'_id': recipe_id})

        recipes = user['recipes']
        # if reciepe not in list already then add, else remove
        if recipe_id not in recipes:
            recipes.append(recipe_id)
        else:
            recipes.remove(recipe_id)

        mongo.db.users.update_one({'_id': user['_id']},{"$set": {'recipes': recipes}}, upsert=True)

        updated_user = mongo.db.users.find_one({'_id': username})
        updated_recipes = updated_user['recipes']

    return redirect(url_for('show_recipe', recipe_id=recipe_id, recipes=updated_recipes))

@app.route('/copy_recipe/<recipe_id>')
@login_required
def copy_recipe(recipe_id): 
    #function for copying someone elses recipe so you can have your own editable version
    recipe = mongo.db.recipes.find_one({'_id': recipe_id})
    owner = mongo.db.users.find_one({'_id': recipe['owner']})
    active_user = mongo.db.users.find_one({'_id': session['username']})
    if session.get('username', None):
        return render_template('edit-recipe.html', recipe=recipe, recipe_id=recipe_id, owner=owner,active_user=active_user)
    else:
        return render_template('recipe.html', recipe=recipe, recipe_id=recipe_id, owner=owner,active_user=active_user)


@app.route('/copy_recipe/<recipe_id>',methods=['GET', 'POST'])
@login_required
def copy_update_recipe(recipe_id):
    #function for updating the copied recipe before its added to the database so you can have your own editable version
    if session.get('username', None):
        #create empty list and add new ingredient for each user added ingredient
        recipe_ingredients = []
        for x in range(1, 41):
            if request.form.get("edit-ingredient-%d" % (x)):
                recipe_ingredients.append(request.form.get("edit-ingredient-%d" % (x)))
        #create empty list and add new step for each user added step
        recipe_steps = []
        for x in range(1, 41):
            if request.form.get("edit-step-%d" % (x)):
                recipe_steps.append(request.form.get("edit-step-%d" % (x)))
        #new recipe id set as variable to be returned to show recipe after it has been added to DB
        hex_id = uuid.uuid4().hex
        recipe_insert = {
            "_id": hex_id,
            'recipe_name': request.form.get('edit-recipient-name'),
            'recipe_description': request.form.get('edit-recipe-description'),
            "recipe_ingredients": recipe_ingredients,
            "recipe_steps": recipe_steps,
            'notes': request.form.get('edit-recipe-notes'),
            "img_url": 'https://res.cloudinary.com/dm2vu1yzr/image/upload/v1597575587/ynfzhoovai1r2jkjjq4l.png',
            'prep_time': request.form.get('edit-prep-time'),
            'cook_time': request.form.get('edit-cook-time'),
            'serves': request.form.get('edit-serves'),
            "difficulty": request.form.get('edit-difficulty'),
            "category": request.form.get('category'),
            "tag": request.form.get('tag'),
            'owner': session['username']
            }

        mongo.db.recipes.insert_one(recipe_insert)

        return redirect(url_for('show_recipe', recipe_id=hex_id, rating_add=False))
    else:
        return redirect(url_for('show_home'))


@app.route('/edit_recipe/<recipe_id>')
@login_required
def edit_recipe(recipe_id): #function to bring up the edit recipe page for the recipe owner to be able to adjust thing within the recipe
    recipe = mongo.db.recipes.find_one({'_id': recipe_id})
    owner = mongo.db.users.find_one({'_id': recipe['owner']})
    active_user = mongo.db.users.find_one({'_id': session['username']})
    if validate_owner(recipe_id) == True:
        return render_template('edit-recipe.html', recipe=recipe, recipe_id=recipe_id, owner=owner, active_user=active_user)
    else:
        return render_template('recipe.html', recipe=recipe, recipe_id=recipe_id, owner=owner,active_user=active_user)


@app.route('/edit_recipe/<recipe_id>',methods=['GET', 'POST'])
@login_required
def update_recipe(recipe_id): #update existing recipe with new entered data from above function
    if validate_owner(recipe_id) == True:
        recipe = mongo.db.recipes.find_one({'_id': recipe_id})
        #create empty list and add new ingredient for each user added ingredient
        recipe_ingredients = []
        for x in range(1, 41):
            if request.form.get("edit-ingredient-%d" % (x)):
                recipe_ingredients.append(request.form.get("edit-ingredient-%d" % (x)))
        #create empty list and add new step for each user added step
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
            "category": request.form.get('category'),
            "tag": request.form.get('tag'),
            'owner': session['username'],
        }}, upsert=True)

        return redirect(url_for('show_recipe', recipe_id=recipe_id))
    
    else:
        return render_template('recipe.html', recipe=recipe, recipe_id=recipe_id,owner=owner)


@app.route('/rate_recipe/<recipe_id>',methods=['GET', 'POST'])
@login_required
def rate_recipe(recipe_id): #allows a user to add a new rating to a recipe or update existing rating is already rated
    recipe = mongo.db.recipes.find_one({'_id': recipe_id})
    owner = mongo.db.users.find_one({'_id': recipe['owner']})

    ratings_rating = []
    owner_ratings_rating = []

    ratings_count = 0
    owner_ratings_count = 0

    if session.get('username', None):
        # if already rated, update rating
        if mongo.db.ratings.find_one({'user_id': session['username'],'recipe_id': recipe['_id']}):
            mongo.db.ratings.update_one({'user_id': session['username'],'recipe_id': recipe['_id']}, {"$set": {'rating': request.form.get('star-rating')}}, upsert=True)
        # add new rating
        else:
            new_rating = {
            "_id": uuid.uuid4().hex,
            "recipe_id": recipe['_id'],
            "owner_id": owner['_id'],
            "user_id": session['username'],
            "rating": request.form.get('star-rating')
            }
            mongo.db.ratings.insert_one(new_rating)

        ratings = mongo.db.ratings.find({'recipe_id': recipe['_id']})
        owner_ratings = mongo.db.ratings.find({'owner_id': owner['_id']})

        try:
        #calculate average rating (rounded for display, unrounded for sorting) for recipe and recipe owner
            for rating in ratings:
                ratings_rating.append(int(rating['rating']))
                ratings_count +=1
                rnd_rating_average = round(sum(ratings_rating)/len(ratings_rating))
                rating_average = float(sum(ratings_rating)/len(ratings_rating))
            mongo.db.recipes.update_one({'_id': recipe['_id']}, {"$set": {
            'rnd_avg_rating': rnd_rating_average,
            'avg_rating': rating_average,
            'count_rating': ratings_count}}, upsert=True)

            for owner_rating in owner_ratings:
                owner_ratings_rating.append(int(owner_rating['rating']))
                owner_ratings_count +=1
                rnd_owner_rating_average = round(sum(owner_ratings_rating)/len(owner_ratings_rating))
                owner_rating_average = float(sum(owner_ratings_rating)/len(owner_ratings_rating))
            mongo.db.users.update_one({'_id': owner['_id']}, {"$set": {
            'rnd_avg_rating': rnd_owner_rating_average,
            'avg_rating': owner_rating_average,
            'count_rating': owner_ratings_count}}, upsert=True)

        except:
            pass
        
        return redirect(url_for('show_recipe', recipe_id=recipe_id, rating_msg=1))
        
    return redirect(url_for('show_recipe', recipe_id=recipe_id, rating_add=False))



@app.route('/search/', methods=['GET', 'POST'])
def search(): #basic search function that will return results based on keyword match to recipe name / description / ingredients
    search_term = request.form.get('input-search')

    if search_term == "":
        return redirect(url_for('show_home'))
    else:
        #create index for searching recipe name / description / ingredients
        search_term = request.form.get('input-search')
        mongo.db.recipes.create_index([('recipe_name', "text"),('recipe_description', "text"),('recipe_ingredients', "text") ])

        #return results by highest rated and then highest vote count
        search_results = mongo.db.recipes.find({"$text": {"$search": search_term}}).sort([('avg_rating', -1), ('count_rating', -1)]).limit(10)

        return render_template('search.html',search_results=search_results, search_term=search_term)


@app.route('/recipes/',methods=['GET', 'POST'])
def all_recipes(): #Simple funciton to display all recipes
    recipes = mongo.db.recipes.find()
    # print(recipes[1])
    return render_template('all-recipes.html',recipes=recipes)


@app.route('/delete/<recipe_id>')
@login_required
def delete_recipe(recipe_id): #function to allow recipe owner to delete the recipe / will allow remove ratings for associated recipe
    if validate_owner(recipe_id) == True:
        username = session['username']
        recipe = mongo.db.recipes.find_one({'_id': recipe_id})
        owner = mongo.db.users.find_one({'_id': recipe['owner']})
        active_user = mongo.db.users.find_one({'_id': username})
        # print(True)
        mongo.db.ratings.delete_many({'recipe_id': recipe['_id']})
        mongo.db.recipes.remove({'_id': recipe['_id']})
# //////////////////////////////////////////////////////////////////////////////
        owner_ratings = mongo.db.ratings.find({'owner_id': owner['_id']})
        try:
            for owner_rating in owner_ratings:
                owner_ratings_rating = []
                owner_ratings_count = 0
                owner_ratings_rating.append(int(owner_rating['rating']))
                owner_ratings_count +=1
                rnd_owner_rating_average = round(sum(owner_ratings_rating)/len(owner_ratings_rating))
                owner_rating_average = float(sum(owner_ratings_rating)/len(owner_ratings_rating))
            mongo.db.users.update_one({'_id': owner['_id']}, {"$set": {
        'rnd_avg_rating': rnd_owner_rating_average,
        'avg_rating': owner_rating_average,
        'count_rating': owner_ratings_count}}, upsert=True)
        except:
            mongo.db.users.update_one({'_id': owner['_id']}, {"$set": {
        'rnd_avg_rating': 0,
        'avg_rating': 0,
        'count_rating': 0}}, upsert=True)
    
    else:
        return redirect(url_for('show_home'))

    return redirect(url_for('dashboard'))



@app.route('/user/update', methods=['GET', 'POST'])
@login_required
def edit_account():
    #allows users to update their acocunt info such as name, pword, email address    
    user = mongo.db.users.find_one({"_id": session['username']})
    if user and pbkdf2_sha256.verify(request.form.get('current-password'), user['password']):
        #check if password and repeat password match
        if request.form.get('new-password') == request.form.get('new-validate-password'):
            # check if user is changing email address
            if user['email'] == request.form.get('email'):
                mongo.db.users.update_one({'_id': session['username']}, {"$set": {
                'name': request.form.get('name'),
                'password': pbkdf2_sha256.encrypt(request.form.get('new-password'))}}, upsert=True)

                user = mongo.db.users.find_one({"_id": session['username']})
                return start_session(user)
            # if you changing email address check its not already in use
            elif mongo.db.users.find_one({"email": request.form.get('email')}):
                return jsonify({"error": "Email address already in use"}), 400

            else:
                mongo.db.users.update_one({'_id': session['username']}, {"$set": {
                'name': request.form.get('name'),
                'email': request.form.get('email'),
                'password': pbkdf2_sha256.encrypt(request.form.get('new-password'))}}, upsert=True)
        
        return jsonify({"error": "Passwords must match"}), 400

    return jsonify({"error": "Current password - Authentication failed"}), 401


def start_session(user):
    #copy of function of same name within user class for use outside of that class - used for edit account to initalise session variable if user information changed
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    session['username'] = session['user']['_id']
    return jsonify(user), 200


@app.route('/user_delete/<user_id>')
@login_required
def delete_account(user_id): 
    #function to allow user to delete their own account and end current session
    if user_id == session['username']:
        mongo.db.users.remove({'_id': user_id})
        session.clear()
        return redirect(url_for('show_home'))
    else:
        return redirect(url_for('show_home'))


def validate_owner(recipe_id):
    #Validate an action that only the recipe owner can do
    # check if active session and set variable to user ID
    try:
        username = session['username']
    except:
        username = ""
    recipe = mongo.db.recipes.find_one({'_id': recipe_id})
    owner = mongo.db.users.find_one({'_id': recipe['owner']})
    active_user = mongo.db.users.find_one({'_id': username})
    #check if the recipe own is the active user
    if owner == active_user:
        return True
    else:
        return False


class Recipe:
#recipe class for adding a new recipe, dynamically adjusts for number of ingredients and steps a user inserts
    def add(self):
        #create empty list and add new ingredient for each user added ingredient
        recipe_ingredients = []
        for x in range(1, 41):
            if request.form.get("ingredient-%d" % (x)):
                recipe_ingredients.append(request.form.get("ingredient-%d" % (x)))
        #create empty list and add new step for each user added step
        recipe_steps = []
        for x in range(1, 41):
            if request.form.get("step-%d" % (x)):
                recipe_steps.append(request.form.get("step-%d" % (x)))
        #recipe object for insertion to DB
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
            "category": request.form.get('category'),
            "tag": request.form.get('tag'),
            "owner": session['username']
        }

        if mongo.db.recipes.insert_one(recipe_insert):
            return jsonify(recipe_insert), 200

        return jsonify({"error": "Add Failed"}), 400

# ////////////////////////////////////////////////////////////////////////////


class User:
#covers basic functions of user such as signing up with new account, logging into an existing account / starting + ending Flask session
    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        session['username'] = session['user']['_id']
        return jsonify(user), 200

    def signup(self):
        #user object for insertion to DB
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
            "recipes": []
        }
    	# check the repeat password matches password
        if request.form.get('password') == request.form.get('validate-password'):
        # encrypt pword
            user['password'] = pbkdf2_sha256.encrypt(user['password'])
        #check if email already exists in DB
            if mongo.db.users.find_one({"email": user['email']}):
                return jsonify({"error": "Email address already in use"}), 400
        # add user to DB
            if mongo.db.users.insert_one(user):
                return self.start_session(user)

            return jsonify({"error": "Signup failed"}), 400
        return jsonify({"error": "Passwords must match"}), 400

    def signout(self):
        # logout function
        session.clear()
        return redirect('/')

    def login(self):
        #login function
        user = mongo.db.users.find_one({"email": request.form.get('email')})
        # validate encryted pword
        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        return jsonify({"error": "Invalid login credentials"}), 401


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
