from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from model.user import UserModel
from extension import db
from forms import register_form, login_form
from werkzeug.security import generate_password_hash, check_password_hash

auth =Blueprint("name", __name__, url_prefix= "/auth")


@auth.route('/register', methods=['GET', 'POST'])
# register a new user
def Register():

# login to an existing account
# logout from a session
# edit user info