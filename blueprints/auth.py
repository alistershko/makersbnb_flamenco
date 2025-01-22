from crypt import methods

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from sqlalchemy.sql.operators import from_
from wtforms.validators import email

from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from model.user import UserModel
from extension import db
from forms import register_form, login_form
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__, url_prefix="/auth")

# Register a new user
@auth.route('/register', methods=['GET', 'POST'])
def Register():
    form = RegisterForm()
    if form.validate_on_submit():
        if UserModel.query.filter_by(email = form.email.data).first():
            flash("Email already exists", "danger")
            return render_template("register.html", form=form)



        user = UserModel(
            username = form.username.data,
            password = form.password.data,
            email = form.email.data,
            phone_number = form.phone_number.data
        )
        db.session.add(user)
        db.session.commit()
        flash("Account create successfully", "success")

        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)

# Login to an existing account
@auth.route('/login', methods = ['GET', 'POST'])
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel().query.filter_by(email = form.email.data)
        if user and user.password() ==  form.password.data:
            # always store the user_id in the session so it temporaily store this information until logout
            session['user_id'] = user.id
            flash("Account Login Successfully", "success")
            return redirect(url_for("main.dashboard"))

        else:
            flash("Password Incorrect", "danger")
    #   redirect to login again
    return render_template("login.html", form=form)

# Logout from a session
@auth.route('/logout')
def Logout():
    session.pop('user_id', None)
    flash("Logged out successfully!", "success")
    return redirect(url_for("auth.login"))

