from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from wtforms.validators import email

from model.booking import BookingModel
from extension import db
from forms import booking_form


bookings = Blueprint("name", __name__, url_prefix= "/bookings")
# make a new booking
@bookings.route('/new', methods=['GET', 'POST'])
def NewBooking():
    form = booking_form()
    if form.validate_on_submit():
        booking = BookingModel(space_id = form.space_id.data,
            requester_id = form.requester_id.data,
            booking_start_date = form.booking_start_date.data,
            booking_end_date = form.booking_end_date.data
        )
        db.session.add(booking)
        db.session.commit()
        flash("Booking submitted", "success")
        return redirect(url_for("bookings.ListBookings"))
    return render_template("new_booking.html", form = form) # We can change the html file name later


# edit an existing booking
@bookings.route('/edit/<int:id>', methods=['GET', 'POST'])
def EditBooking(id):
    booking = BookingModel.query.get(id) #fetch bookings by id
    if request.method == 'POST':
        # Update booking with submitted form data
        booking.space_id = request.form['space_id']
        booking.requester_id = request.form['requester_id']
        booking.booking_start_date = request.form['booking_start_date']
        booking.booking_end_date = request.form['booking_end_date']
        db.session.commit()
        flash("Booking updated", "success")
        return redirect(url_for("bookings.ListBookings"))
    return render_template("edit_booking.html", booking = booking) # We can change the html file name later


# delete an existing booking
@bookings.route('/delete/<int:id>', methods=['POST'])
def DeleteBooking(id):
    booking = BookingModel.query.get(id)
    db.session.delete(booking)
    db.session.commit()
    flash("Booking deleted", "success")
    return redirect(url_for("bookings.ListBookings"))


# list all bookings
@bookings.route('/list_all', methods=['GET'])
def ListBookings():
    bookings = BookingModel.query.all()
    return render_template("list_bookings.html", bookings = bookings)


# list one booking
@bookings.route('list_one/<int:id>', methods=['GET'])
def OneBooking(id):
    booking = BookingModel.query.get(id)
    return render_template("list_one_booking.html", booking = booking)