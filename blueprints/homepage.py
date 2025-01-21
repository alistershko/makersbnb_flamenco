from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from model.space import SpaceModel
from extension import db
from forms import space_form
from werkzeug.security import generate_password_hash, check_password_hash

# list all existing spaces
# show one specific space
# request to book a specific space

homepage =Blueprint("name", __name__, url_prefix= "/homepage")

# route路由，下面定义的是视图函数view function, 所以url_for('homepage.ListAllSpace')
@homepage.route('/all', methods=['GET'])
def ListAllSpaces():
    spaces = SpaceModel.query.all()
    return render_template('all_spaces.html', spaces = spaces)


@homepage.route('/spaces/<int:space_id>', methods=['GET'])
def ShowOneSpace(space_id):
    space = SpaceModel.query.filter_by(space_id)
    if not space:
        flash("space not found", "danger")
        return redirect(url_for('homepage.ListAllSpaces'))
    return render_template('single_space.html', space = space)
