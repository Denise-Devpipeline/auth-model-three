from flask import request, Blueprint

from controllers import user_controller

user = Blueprint('user', __name__)


@user.route('/user/update/<id>', methods=["PUT"])
def update_user(id):
    return user_controller.update_user(id)


@user.route('/user/add', methods=["POST"])
def add_user():
    return user_controller.add_user()


@user.route('/user/get', methods=["GET"])
def get_all_active_users():
    return user_controller.get_all_active_users()


@user.route('/user/get/<id>', methods=["GET"])
def get_users_by_id(id):
    return user_controller.get_users_by_id(id)
