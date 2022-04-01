#não utilizada no momento
from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return "<h3>Login</h3>"