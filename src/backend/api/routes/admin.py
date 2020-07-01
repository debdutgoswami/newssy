from flask import request, make_response, jsonify

from api.routes import api
from api.routes.auth import token_required

from api.models import db
from api.models.users import User
from api.models.news import News

from api.email.tasks import deliver_email

import datetime

@api.route('/admin/users')
@token_required
def admin_users(current_user):
    """User List

    Request Type:
        GET

    HEADERS:
        x-access-token -- JWT

    Returns:
        responseObject -- success (list of users along with their details)

    Response Code:
        201 -- success
    """
    users = User.query.all()

    final = list()
    for user in users:
        final.append({
            'public_id' : user.public_id,
            'first_name': user.first_name,
            'last_name' : user.last_name,
            'email'     : user.email,
            'joined_on' : user.joined_on,
            'verified'  : user.VERIFIED
        })

    return make_response({
        'status' : 'success',
        'message': final
    }, 201)

@api.route('/admin/ban')
@token_required
def admin_ban(current_user):
    """BAN USER

    Request Type:
        GET

    HEADERS:
        x-access-token -- JWT

    BODY:
        public_id -- public id of the user to be banned
        action (boolean) -- True: BAN   False: UN-BAN

    Returns:
        responseObject -- success or failure

    Response Code:
        201 -- success
        401 -- fail
    """
    public_id = request.get_json(silent=True).get('public_id')
    action = request.get_json(silent=True).get('action')

    try:
        action = bool(action)
    except ValueError:
        return make_response({
            'status' : 'fail',
            'message': 'Wrong Payload!! Supply only Boolean!!'
        }, 401)

    user = User.session.filter_by(public_id=public_id).first()

    if user:
        try:
            # email queue
            deliver_email.delay(
                template='banned.html',
                subject='IMPORTANT: BANNED',
                name=user.first_name,
                email=user.email,
                link=""
            )
            # actions on DB
            user.BANNED = bool(action)
            user.banned_on = datetime.datetime.utcnow()
            db.session.commit()

            return make_response({
                'status' : 'success',
                'message': 'User successfully banned'
            }, 201)
        except:
            return make_response({
                'status' : 'fail',
                'message': 'Some error occured!!'
            }, 401)
        
    else:
        return make_response({
            'status' : 'fail',
            'message': 'User not found!!'
        }, 401)

@api.route('/admin/remove/<public_id>')
@token_required
def admin_remove(current_user, public_id):
    pass