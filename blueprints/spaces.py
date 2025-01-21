from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from model.user import UserModel
from extension import db
from forms import *
from werkzeug.security import generate_password_hash, check_password_hash

spaces =Blueprint("name", __name__, url_prefix= "/spaces")

@spaces.route('/make_a_new_space', methods=['GET', 'POST'])
def MakeASpace():
    space_form = SpaceForm()
    if space_form.validate_on_sumbit():

        if SpaceModel.query.filter_by(location=form.location.data).first():
            flash("")
        


@spaces.route('/edit_an_existing_space', methods=['GET', 'POST'])

@spaces.route('/delete_an_existing_space', methods=['GET', 'POST'])

@spaces.route('/list_all_spaces', methods=['GET', 'POST'])

@spaces.route('/list_one_space', methods=['GET', 'POST'])




# make a new space
# edit an existing space
# delete an existing space
# list all spaces
# list one space