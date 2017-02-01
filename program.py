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


# Create a new recipe group
@app.route('/recipe-groups/new/', methods=['GET', 'POST'])
def newRecipeGroup():
    if request.method == 'POST':
        newRecipeGroup = RecipeGroup(name=request.form['name'])
        session.add(newRecipeGroup)
        session.commit()
        return redirect(url_for('showRecipeGroups'))
    else:
        return render_template('new-recipe-group.html')
        # return "This page will be for making a new restaurant"


# edit recipe group
@app.route('/recipe-groups/<int:recipe_group_id>/edit/', methods=['GET', 'POST'])
def editRecipeGroup(recipe_group_id):
    editedRecipeGroup = session.query(
        RecipeGroup).filter_by(id=recipe_group_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRecipeGroup.name = request.form['name']
            return redirect(url_for('showRecipeGroups'))
    else:
        return render_template(
            'edit-recipe-group.html', recipe_group=editedRecipeGroup)




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
