from controllers import auth_controller

from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.route("/user/auth", methods=["POST"])
def auth_token_add():
    return auth_controller.auth_token_add()
