from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, RecipeGroup, Recipe
from datetime import datetime

app = Flask(__name__)

engine = create_engine('sqlite:///recipes.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


""" Setup athor info """
# author url
@app.context_processor
def inject_authorUrl():
    return {'url': 'http://buildcreativewebsites.com'}

# copyright year
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


# Show recipe groups
@app.route('/')
@app.route('/recipe-groups/')
def showRecipeGroups():
    recipe_groups = session.query(RecipeGroup).all()
    # return "This page will show all my restaurants"
    return render_template('recipe-groups.html', recipe_groups=recipe_groups)


# show recipes in group
@app.route('/recipe-group/<int:recipe_group_id>/')
@app.route('/recipe-group/<int:recipe_group_id>/recipes/')
def showRecipes(recipe_group_id):
    recipe_group = session.query(RecipeGroup).filter_by(id=recipe_group_id).one()
    recipes = session.query(Recipe).filter_by(
        recipe_group_id=recipe_group_id).all()
    return render_template('recipes.html', recipes=recipes, recipe_group=recipe_group)


if __name__ == '__main__':
    app.run(debug=True)
