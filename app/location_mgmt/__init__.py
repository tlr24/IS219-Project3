import csv
import json
import logging
import os

from flask import Blueprint, render_template, abort, url_for, current_app, jsonify, flash
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from app.db import db
from app.db.models import Location
from app.auth.decorators import admin_required
from app.location_mgmt.forms import location_edit_form, add_location_form
from werkzeug.utils import secure_filename, redirect
from flask import Response


locations = Blueprint('locations', __name__,
                        template_folder='templates')

@locations.route('/locs/<int:loc_id>')
@login_required
def retrieve_location(loc_id):
    location = Location.query.get(loc_id)
    return render_template('loc_view.html', location=location)


@locations.route('/locs/<int:loc_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_location(loc_id):
    location = Location.query.get(loc_id)
    form = location_edit_form(obj=location)
    if form.validate_on_submit():
        location.title = form.title.data
        location.longitude = form.longitude.data
        location.latitude = form.latitude.data
        location.population = int(form.population.data)
        db.session.add(location)
        db.session.commit()
        flash('Location Edited Successfully', 'success')
        current_app.logger.info("edited a location")
        return redirect(url_for('map.location_datatables'))
    return render_template('loc_edit.html', form=form)


@locations.route('/locs/new', methods=['POST', 'GET'])
@login_required
def add_location():
    form = add_location_form()
    if form.validate_on_submit():
        location = Location.query.filter_by(title=form.title.data).first()
        if location is None:
            location = Location(title=form.title.data, longitude=form.longitude.data, latitude=form.latitude.data, population=int(form.population.data))
            db.session.add(location)
            db.session.commit()
            flash('Location added successfully', 'success')
            return redirect(url_for('map.browse_locations'))
        else:
            flash('Location with same title already exists')
            return redirect(url_for('map.browse_locations'))
    return render_template('loc_add.html', form=form)


@locations.route('/locs/<int:loc_id>/delete', methods=['POST'])
@login_required
def delete_location(loc_id):
    location = Location.query.get(loc_id)
    #if location.id == current_user.id:
        #flash("You can't delete yourself!")
        #return redirect(url_for('auth.browse_users'), 302)
    db.session.delete(location)
    db.session.commit()
    flash('Location Deleted', 'success')
    return redirect(url_for('map.browse_locations'), 302)
