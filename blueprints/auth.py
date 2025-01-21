from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from wtforms.validators import email

from model.user import UserModel
from extension import db
from forms import register_form, login_form
from werkzeug.security import generate_password_hash, check_password_hash

auth =Blueprint("name", __name__, url_prefix= "/auth")


@auth.route('/register', methods=['GET', 'POST'])
# register a new user
def Register():
    form = register_form()
    if form.validate_on_submit():
        if UserModel.query.filter_by(email = form.email.data).first():
            flash("Email already exists", "danger")
            return None

        user = UserModel(username = form.username.data,
                         password = form.password.data,
                         email = form.email.data,
                         phone_number = form.phone_number.data
                         )




# login to an existing account
# logout from a session
# edit user info