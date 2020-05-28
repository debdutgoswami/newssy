from flask import request, make_response, jsonify

from api.routes import api
from api.routes.auth import token_required

@api.route('/admin/users')
@token_required
def admin_users(current_user):
    pass

@api.route('/admin/scrapers')
@token_required
def admin_scrapers(current_user):
    pass

@api.route('/admin/ban/<public_id>')
@token_required
def admin_ban(current_user, public_id):
    pass

@api.route('/admin/remove/<public_id>')
@token_required
def admin_remove(current_user, public_id):
    pass