from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from . import db, login_manager
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=True)
    expense_categories = db.relationship("ExpenseCategories", backref="user")

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"confirm": self.id}).decode("utf-8")

    def confirm(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except:
            return False
        if data.get("confirm") != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"reset": self.id}).decode("utf-8")

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except:
            return False
        user = User.query.get(data.get("reset"))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def __repr__(self):
        return "<User %r>" % self.username


class Balances(User):
    __tablename__ = "balances"
    balance = db.Column(db.Float, default=0.00)
    db.relationship("Expenses", backref="balance")
    db.relationship("Incomes", backref="balance")

    def __repr__(self):
        return f"<Balance of {self.username} - {self.balance}>"


class ExpenseCategories(db.Model):
    __tablename__ = "expense_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, index=True)
    description = db.Column(db.String(200), index=True)
    expenses = db.relationship("Expenses", backref="expense_category")

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"<ExpenseCategory {self.name}>"


class Expenses(db.Model):
    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("expense_categories.id"))
    name = db.Column(db.String(50), unique=True, index=True)
    description = db.Column(db.String(200), index=True)
    date = db.Column(db.DateTime, default=datetime.now)
    amount = db.Column(db.Float)

    def __repr__(self):
        return f"<Expense {self.name} - {self.amount}>"


class IncomeCategories(db.Model):
    __tablename__ = "income_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, index=True)
    description = db.Column(db.String(200), index=True)
    incomes = db.relationship("Incomes", backref="income_category")

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"<IncomeCategory {self.name}>"


class Incomes(db.Model):
    __tablename__ = "incomes"
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("income_categories.id"))
    name = db.Column(db.String(50), unique=True, index=True)
    description = db.Column(db.String(200), index=True)
    amount = db.Column(db.Float)

    def __repr__(self):
        return f"<Income {self.name} - {self.amount}>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
