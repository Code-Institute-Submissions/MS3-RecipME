import os
from bson.objectid import ObjectId
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo

# Local deploy only
from os import path
if path.exists("env.py"):
    import env


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'cookbook'
app.config["MONGO_URI"] = os.getenv('MONGO_URI')
# app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost') #Heroku Deplyment


mongo = PyMongo(app)


@app.route('/')
@app.route('/home')
def show_home():
    return render_template('index.html',
                           recipes=mongo.db.recipes.find())


@app.route('/recipe/<recipe_id>')
def show_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('recipe.html', recipe=recipe)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
