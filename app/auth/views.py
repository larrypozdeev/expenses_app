from .forms import LoginForm, RegistrationForm
from flask import render_template, flash, redirect, url_for
from . import auth
from .. import db
from ..models import User


@auth.route("/login", methods=["GET", "POST"])
def login():
    return render_template("auth/login.html", form=LoginForm())


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
