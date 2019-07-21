# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from my_flask_app.user.forms import DomainForm
from my_flask_app.user.models import Domain
from my_flask_app.utils import flash_errors

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    """List members."""
    return render_template("users/members.html")


@blueprint.route('/add_domain', methods=['GET', 'POST'])
def add_domain():
    if request.method == 'GET':
        return render_template('users/add_domain.html', form=DomainForm())
    else:

        form = DomainForm(request.form)
        if form.validate_on_submit():
            Domain.create(domain=form.domain.data, description=form.desc.data, user=current_user)
        else:
            flash_errors(form)
        return render_template('users/add_domain.html', form=DomainForm())
