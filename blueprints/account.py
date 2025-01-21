

# list all owned spaces
# list all approved bookings
# list all pending requests
# make a new space
# edit an existing owned space
# delete an existing owned space


@spaces.route('/make_a_new_space', methods=['GET', 'POST'])
def MakeASpace():
    form = SpaceForm()
    if form.validate_on_sumbit():
        if SpaceModel.query.filter_by(location=form.location.data).first():
            flash("The location you are attempting to submit is already associated with an existing space", "danger")
            return None
        
        new_space = SpaceModel(
            name = form.name.data,
            description = form.description.data,
            location = form.location.data,
            price_per_night = form.price_per_night.data
        )
        db.session.add(new_space)
        db.session.commit()

        flash("New space successfuly listed!", "success")
        return None
    return render_template("make_a_new_space.html", form=form)

# @spaces.route('/edit_an_existing_space', methods=['GET', 'POST'])

# @spaces.route('/delete_an_existing_space', methods=['GET', 'POST'])