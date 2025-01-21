from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from wtforms.validators import email
from model.space import SpaceModel
from model.user import *
from model.request import *
from extension import db
from forms import approve_request_form, booking_request_form



requests =Blueprint("name", __name__, url_prefix= "/requests")

@requests.route('/user_requests', methods=['GET'])
def user_requests():
    if 'user_id' not in session:
        flash("You need to be logged in to view your requests.", "danger")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user = UserModel.query.get(user_id)

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))

    requests_made = RequestModel.query.filter_by(requester_id=user_id).all()
    requests_received = RequestModel.query.join(SpaceModel).filter(SpaceModel.owner_id == user_id).all()

    return render_template('user_requests.html', requests_made=requests_made, requests_received=requests_received)


@requests.route('/make_request', methods=['GET', 'POST'])
def make_request():
    if 'user_id' not in session:
        flash("You need to be logged in to make a request.", "danger")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        user_id = session['user_id']
        space_id = request.form.get('space_id')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        message = request.form.get('message')

        new_request = RequestModel(
            requester_id=user_id,
            space_id=space_id,
            start_date=start_date,
            end_date=end_date,
            message=message
        )

        db.session.add(new_request)
        db.session.commit()

        flash("Request made successfully.", "success")
        return redirect(url_for('requests.user_requests'))

    spaces = SpaceModel.query.all()
    return render_template('make_request.html', spaces=spaces)






# make a new request
# edit an existing request
# delete an existing request
# list all request
# list one request