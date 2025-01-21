from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from model.space import SpaceModel
from extension import db
from forms import space_form
from werkzeug.security import generate_password_hash, check_password_hash

homepage =Blueprint("name", __name__, url_prefix= "/homepage")

@homepage.route('/all', methods=['GET'])
def ListAllSpaces():
    pass

@homepage.route('/the_name_of_the_space', methods=['GET'])
def ShowOneSpace():
    pass