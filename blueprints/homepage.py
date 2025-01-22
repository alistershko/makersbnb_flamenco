from crypt import methods
from pyexpat.errors import messages

from flask import Blueprint, render_template, redirect, url_for, flash, request, session

from blueprints.requests import requests
from blueprints.spaces import spaces
from forms.booking_request_form import BookingRequestForm
from model import RequestModel, BookingModel
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

# owner checking pending request

@homepage.route('spaces/<int:space_id>/request', methods = ['GET', 'POST'])
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

# owner need to check the requests from other users
@homepage.route('owners/request')
def OwnerViewRequests():
    owner_space_ids = [space.id for space in SpaceModel.query.filter_by(owner_id = session['user_id'])]
    pending_requests = RequestModel.query.filter(
        RequestModel.space_id.in_(owner_space_ids),
        RequestModel.status == "pending"
    ).all()
    return render_template('owner_requests.html', request = pending_requests)



# owner can approve the request
@homepage.route('request/<int:request_id/approve>', methods = ['POST'])
def ApproveRequest(request_id):
    request = RequestModel.query.filter_by(id = request_id)
    if not request:
        flash("Request not found.", "error")
        return redirect(url_for('homepage.ViewRequests'))
    booking = BookingModel(
        space_id = request.space_id,
        requester_id = request.request_id,
        booking_start_date = request.booking_start_date,
        booking_end_date = request.booking_end_date
    )
    db.session.add(booking)
    db.session.commit()
    flash("Request approved and booking created.", "success")
    return redirect(url_for('homepage.ViewRequests'))

# owner reject the request

@homepage.route('/request/<int:request_id>/reject', methods=['POST'])
def RejectRequest(request_id):
    request = RequestModel.query.get(request_id)
    if not request:
        flash("Request not found.", "error")
        return redirect(url_for('homepage.ViewRequests'))

    request.status = "Rejected"
    db.session.commit()
    flash("Request rejected.", "info")
    return redirect(url_for('homepage.ViewRequests'))


# pending requests
@homepage.route('<int:user_id>/requests')
def RequesterViewRequest(user_id):
    requests = RequestModel.query.filter_by(requester_id = user_id).all()
    return render_template('user_requests.html', requests=requests)

@homepage.route('/<int:user_id>/bookings', methods=['GET'])
def RequesterViewBooking(user_id):
    bookings = BookingModel.query.filter_by(user_id=user_id).all()


    return render_template('user_bookings.html', bookings=bookings)




