from flask_login.utils import login_required
from .forms import LoginForm, RegistrationForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user
from . import auth
from .. import db
from ..models import User


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.is_submitted():
        user = User(
            email=form.email.data.lower(),
            username=form.username.data.lower(),
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        # send_email(
        #     user.email,
        #     "Confirm Your Account",
        #     "auth/email/confirm",
        #     user=user,
        #     token=token,
        # )
        flash("A confirmation email has been sent to you by email.")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.is_submitted():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for("budget.index")
            return redirect(next)
        flash("Invalid email or password.")
    return render_template("auth/login.html", form=form)


@auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("budget.index"))
