from crypt import methods
from pyexpat.errors import messages

from flask import Blueprint, render_template, redirect, url_for, flash, request, session


from forms.booking_request_form import BookingRequestForm
from model import RequestModel, BookingModel
from model.space import SpaceModel
from extension import db
from forms import space_form
from werkzeug.security import generate_password_hash, check_password_hash

account =Blueprint("name", __name__, url_prefix= "/account")

# View requests for spaces user owns
@account.route('/request', methods = ['GET'])
def ViewRequestsAsOwner():
    owner_space_ids = [space.id for space in SpaceModel.query.filter_by(owner_id = session['user_id'])]
    pending_requests = RequestModel.query.filter(
        RequestModel.space_id.in_(owner_space_ids),
        RequestModel.status == "pending"
    ).all()
    return render_template('owner_requests.html', request = pending_requests)

# Approve a request as an owner
@account.route('/request/<int:request_id/approve>', methods = ['POST'])
def ApproveRequestAsOwner(request_id):
    request = RequestModel.query.filter_by(id = request_id)
    if not request:
        flash("Request not found.", "error")
        return redirect(url_for('account.ViewRequestsAsOwner'))
    booking = BookingModel(
        space_id = request.space_id,
        requester_id = request.request_id,
        booking_start_date = request.booking_start_date,
        booking_end_date = request.booking_end_date
    )
    request.status = "Approved"
    db.session.add(booking)
    db.session.commit()
    flash("Request approved and booking created.", "success")
    return redirect(url_for('account.ViewRequestsAsOwner'))

# Reject a request as an owner
@account.route('/request/<int:request_id>/reject', methods=['POST'])
def RejectRequestAsOwner(request_id):
    request = RequestModel.query.get(request_id)
    if not request:
        flash("Request not found.", "error")
        return redirect(url_for('account.ViewRequestsAsOwner'))

    request.status = "Rejected"
    db.session.commit()
    flash("Request rejected.", "info")
    return redirect(url_for('account.ViewRequestsAsOwner'))

# View requests for spaces user has requested to book
@account.route('<int:user_id>/requests', methods = ['GET'])
def ViewRequestsAsRequester(user_id):
    requests = RequestModel.query.filter_by(requester_id = user_id).all()
    return render_template('user_requests.html', requests=requests)

# View bookings for spaces user has booked
@account.route('/<int:user_id>/bookings', methods = ['GET'])
def ViewBookingsAsRequester(user_id):
    bookings = BookingModel.query.filter_by(user_id=user_id).all()
    return render_template('user_bookings.html', bookings=bookings)

