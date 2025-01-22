from crypt import methods
from pyexpat.errors import messages

from flask import Blueprint, render_template, redirect, url_for, flash, request, session


from forms.booking_request_form import BookingRequestForm
from model import RequestModel, BookingModel
from model.space import SpaceModel
from extension import db
from forms import space_form
from werkzeug.security import generate_password_hash, check_password_hash


homepage =Blueprint("homepage", __name__, url_prefix= "/homepage")

# Show all spaces on the homepage
@homepage.route('/all', methods=['GET'])
def ListAllSpaces():
    spaces = SpaceModel.query.all()
    return render_template('all_spaces.html', spaces = spaces)


# Show one specific space
@homepage.route('/spaces/<int:space_id>', methods=['GET'])
def ShowOneSpace(space_id):
    space = SpaceModel.query.filter_by(space_id)
    if not space:
        flash("space not found", "danger")
        return redirect(url_for('homepage.ListAllSpaces'))
    return render_template('single_space.html', space = space)

# Make a request to book a specific space
@homepage.route('/spaces/<int:space_id>/request', methods = ['GET', 'POST'])
def RequestToBook(space_id):
    form = BookingRequestForm()
    if form.validate_on_submit():
        new_request = RequestModel(
            space_id = space_id,
            requester_id = session['user_id'],
            messages = form.message.data,
            booking_start_date = form.booking_start_date.data,
            booking_end_date = form.booking_end_date.data
        )
        db.session.add(new_request)
        db.session.commit()
        flash("Your booking request has been submitted", "success")
        return redirect(url_for('homepage.ShowOneSpace', space_id=space_id))
    return render_template('request_form.html', form=form, space_id=space_id)

