from flask import Flask, request, jsonify
from conn import *


def org_create(post_data):
    name = post_data['first_name']
    phone = post_data['phone']
    city = post_data['city']
    state = post_data['state']
    active = post_data['active']

    cursor.execute(
        """INSERT INTO ORGANIZATIONS (name, phone, city, state, active) VALUES (%s,%s,%s,%s,%s)""", [name, phone, city, state, active])

    conn.commit()
    return jsonify("Organization Created"),  201


def all_active_orgs():
    cursor.execute(
        "SELECT org_id, name, phone, city, state, active FROM Organizations WHERE active =1")
    results = cursor.fetchall()
    if not results:
        return jsonify("No active Organizations to return"), 404
    else:
        active_orgs_result = []
        for result in results:
            results_dict = {
                'org_id': result[0],
                'name': result[1],
                'phone': result[2],
                'city': result[3],
                'state': result[4],
                'active': result[5]
            }
            active_orgs_result.append(results_dict)
        return jsonify(active_orgs_result), 200


def get_org_by_id(org_id):
    cursor.execute("SELECT org_id, name, phone, city, state, active FROM Organizations WHERE org_id = %s;",
                   [org_id])
    result = cursor.fetchone()
    if not result:
        return jsonify("That organization does not exist."), 404
    else:
        results_dict = {
            'org_id': result[0],
            'name': result[1],
            'phone': result[2],
            'city': result[3],
            'state': result[4],
            'active': result[5]
        }
        return jsonify(results_dict), 200


def activate_org(org_id):
    cursor.execute(
        "UPDATE Organizations SET active = 1 WHERE org_id = %s", [org_id])
    conn.commit()
    return jsonify("Organization Activated!"), 200


def deactivate_org(org_id):
    cursor.execute(
        "UPDATE Organizations SET active = 0 WHERE org_id = %s", [org_id])
    conn.commit()
    return jsonify("Organization Deactivated!"), 200


def org_update_by_id(org_id, post_data):
    cursor.execute("SELECT org_id, name, phone, city, state, active FROM Organizations WHERE org_id = %s;",
                   [org_id])
    result = cursor.fetchone()
    if not result:
        return jsonify("Organization does not exist."), 404
    else:
        result_dict = {
            'org_id': result[0],
            'name': result[1],
            'phone': result[2],
            'city': result[3],
            'state': result[4],
            'active': result[5]
        }

    for key, val in post_data.copy().items():
        if not val:
            post_data.pop(key)
    result_dict.update(post_data)

    cursor.execute('''UPDATE Organizations SET 
    name = %s,
    phone = %s,
    city = %s,
    state = %s,
    active = %s
    WHERE org_id = %s;
    ''',
                   [result_dict['name'],
                    result_dict['phone'],
                    result_dict['city'],
                    result_dict['state'],
                    result_dict['active'],
                    result_dict['org_id']])
    conn.commit()
    return jsonify("Organization Updated!")


def delete_org(org_id):
    cursor.execute("DELETE FROM Organizations WHERE org_id = %s", [org_id])
    conn.commit()
    return jsonify("Organization Deleted!"), 200
