from flask import request, Blueprint

from controllers import org_controller

org = Blueprint('org', __name__)


@org.route('/orgs/add', methods=["POST"])
def add_organization():
    return org_controller.add_organization()


@org.route('/org/get/<id>', methods=["GET"])
def get_org_by_id(id):
    return org_controller.get_org_by_id(id)


@org.route('/orgs/get', methods=["GET"])
def get_all_orgs():
    return org_controller.get_all_orgs()
