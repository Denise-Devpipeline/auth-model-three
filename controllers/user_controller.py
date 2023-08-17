from flask import Request, Response, jsonify
from flask_bcrypt import generate_passport_hash

from db import db
from models.users import Users, user_schema, users_schema
from util.reflection import populate_object


# GET ALL Customers  This part, down to create section is from Foundations.
def users_get_all(req: Request, auth_info) -> Response:
    if permission_check(auth_info, 'users_read_all'):
        users_query = db.session.query(AppUsers).order_by(AppUsers.last_name.asc()).order_by(AppUsers.first_name.asc()).all()

    elif permission_check(auth_info, 'users_read_organization'):
        users_query = db.session.query(AppUsers).filter(
            AppUsers.org_id == auth_info.user.org_id).filter(AppUsers.active == True).order_by(
            AppUsers.last_name.asc()).order_by(
            AppUsers.first_name.asc()).all()
    else:
        return jsonify({'message': 'invalid permissions'}), 403

    list_of_users = []

    for user in users_query:
        user = append_custom_fields(user_schema.dump(user), user.user_id)
        list_of_users.append(user)

    return jsonify({"message": "users found", "users":  list_of_users}), 200


# CREATE
def update_user(id):
    req_data = request.form if request.form else request.json
    existing_user = db.session.query(Users).filter(Users.user_id == id).first()

    new_user = Users.new_user
    populate_object(existing_user, req_data)

    new_user.password = generate_passport_hash(new_user.password).decode('utf8')

    db.session.commit()

    return jsonify("User Created"), 200


def add_user():
    req_data = request.form if request.form else request.json

    if not req_data:
        return jsonify("Please enter all the required fields"), 401

    new_user = Users.new_user()

    populate_object(new_user, req_data)

    new_user.password = generate_passport_hash(new_user.password).decode('utf8')

    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user)), 200

# READ


def get_all_active_users(request):
    users = db.session.query(Users).filter(Users.active == True).all()

    if not users:
        return jsonify('No Users Exist'), 404

    else:
        return jsonify(users_schema.dump(users)), 200


def get_users_by_id(id):
    user = db.session.query(Users).filter(Users.user_id == id).first()

    if not user:
        return jsonify("That user does not exist"), 404

    else:
        return jsonify(user_schema.dump(user)), 200

# UPDATE


def update_user(id):
    req_data = request.form if request.form else request.json
    existing_user = db.session.query(Users).filter(Users.user_id == id).first()
    populate_object(existing_user, req_data)

    existing_user.password = generate_password_hash(existing_user.password).decode('utf8')

    db.session.commit()

    return jsonify('User Created'), 200

# DEACTIVATE/ACTIVATE

# DELETE
