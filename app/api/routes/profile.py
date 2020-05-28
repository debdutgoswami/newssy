from flask import request, make_response, jsonify

from api.routes import api
from api.routes.auth import token_required

from api.models import users, news

@api.route('/profile-data', methods=['POST'])
@token_required
def profile_data(current_user):
    return make_response(jsonify({
        'status' : 'success',
        'message': 'Pong'
    }))

@api.route('/change-name', methods=['PUT'])
@token_required
def change_name(current_user):
    pass

@api.route('/change-preference', methods=['PUT'])
@token_required
def change_preference(current_user):
    pass

@api.route('/email-notification', methods=['PUT'])
@token_required
def email_notification(current_user):
    pass

@api.route('/whatsapp-notification', methods=['PUT'])
@token_required
def whatsapp_notification(current_user):
    pass

@api.route('/change-email', methods=['PUT'])
@token_required
def change_email(current_user):
    pass

@api.route('/show-saved-article')
@token_required
def saved_article(current_user):
    pass