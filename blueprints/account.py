from crypt import methods
from pyexpat.errors import messages

from flask import Blueprint, render_template, redirect, url_for, flash, request, session

from forms.booking_request_form import BookingRequestForm
from model import RequestModel, BookingModel
from model.space import SpaceModel
from extension import db
from forms import space_form
from werkzeug.security import generate_password_hash, check_password_hash

account =Blueprint("account", __name__, url_prefix= "/account")

@account.route('/request', methods=['GET'])
def ViewRequestsAsOwner():
    # Get current user id
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to view requests.", "error")
        return redirect(url_for('auth.login'))

    # Find all spaces owned by the user
    owner_space_ids = [space.id for space in SpaceModel.query.filter_by(owner_id=user_id).all()]
    print("Owner Space IDs:", owner_space_ids)  # Testing output

    # Return empty list if user does not own any spaces
    if not owner_space_ids:
        flash("You do not own any spaces.", "info")
        return render_template('owner_requests.html', requests=[])

    # Enquire any related space requests
    pending_requests = RequestModel.query.filter(
        RequestModel.space_id.in_(owner_space_ids),
        RequestModel.status == "pending"
    ).all()
    print("Pending Requests:", pending_requests)  # testing output

    return render_template('owner_requests.html', requests=pending_requests)

# Approve a request as an owner
@account.route('/request/<int:request_id>/<string:action>', methods=['POST'])
def HandleRequestAsOwner(request_id, action):
    # Find request
    request = RequestModel.query.get(request_id)
    if not request:
        flash("Request not found.", "error")
        return redirect(url_for('account.ViewRequestsAsOwner'))

    # follow action to determine logic for next step
    if action == "approve":
        booking = BookingModel(
            space_id=request.space_id,
            requester_id=request.requester_id,
            booking_start_date=request.booking_start_date,
            booking_end_date=request.booking_end_date
        )
        request.status = "Approved"
        db.session.add(booking)
        flash("Request approved and booking created.", "success")
    elif action == "reject":
        request.status = "Rejected"
        flash("Request rejected.", "info")
    else:
        flash("Invalid action.", "error")
        return redirect(url_for('account.ViewRequestsAsOwner'))

    # commit changes to database
    db.session.commit()
    return redirect(url_for('account.ViewRequestsAsOwner'))

# View requests for spaces user has requested to book
@account.route('/requests', methods=['GET'])
def ViewRequestsAsRequester():
    requests = RequestModel.query.filter_by(requester_id=session['user_id']).all()
    return render_template('user_requests.html', requests=requests)

# View bookings for spaces user has booked
@account.route('/bookings', methods=['GET'])
def ViewBookingsAsRequester():
    bookings = BookingModel.query.filter_by(requester_id=session['user_id']).all()
    return render_template('user_bookings.html', bookings=bookings)
