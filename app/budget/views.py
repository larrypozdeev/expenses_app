from flask import render_template
from flask_login.utils import login_required, current_user
from . import budget
from ..models import Balances


@login_required
@budget.route("/overview", methods=["GET"])
def index():
    balance = Balances.query.filter_by(id=current_user.id).first().balance
    return render_template("budget/overview.html", balance=balance)
