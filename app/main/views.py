from flask import render_template
from flask_login.utils import login_required, current_user
from sqlalchemy.sql.elements import and_
from . import main
from ..models import Balances, Expenses
from datetime import date, timedelta
from sqlalchemy import and_


@main.route("/", methods=["GET"])
def index():
    return render_template("index.html")
