from flask import request,make_response, jsonify, url_for
import uuid, jwt, datetime
from functools import wraps
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

from api import app, db, bcrypt
from api.routes import api
from api.models.users import User
from api.email.tasks import deliver_contact_email


urlsafe = URLSafeTimedSerializer(app.config.get('SECRET_KEY'))

# checking whether loged-in or not based on that info, data is provided
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!!'}), 401

        return  f(current_user, *args, **kwargs)

    return decorated

@api.route('/signup', methods=['POST'])
def signup():
    data = request.form

    name, email, password = data.get('name'), data.get('email'), data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        try:
            # email Queue
            token = urlsafe.dumps(email, salt='email-confirm')
            deliver_contact_email.delay(
                subject='IMPORTANT: EMAIL CONFIRMATION',
                name=name,
                email=email,
                link=f"http://localhost:5000/api/confirm/{token}"
            )

            user = User(
                name=name,
                email=email,
                password=password
            )
            # insert user
            db.session.add(user)
            db.session.commit()

            """TODO
                Setup email Queue using Celery and Redis
            """

            responseObject = {
                'status': 'success',
                'message': 'Successfully registered.'
            }

            return make_response(jsonify(responseObject), 201)
        except Exception:
            responseObject = {
                'satus': 'fail',
                'message': 'Some error occured. Please try again.'
            }

            return make_response(jsonify(responseObject), 401)
    else:
        responseObject = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.'
        }

        return make_response(jsonify(responseObject), 202)

@api.route('/confirm/<token>', methods=['GET'])
def confirm(token):
    try:
        email = urlsafe.loads(token, salt='email-confirm', max_age=3600)
        user = User.query.filter_by(email=email).first()

        if user:
            user.confirmed=True

            responseObject = {
            'status': 'success',
            'message': 'Email successfully confirmed'
            }

            return make_response(jsonify(responseObject), 201)

        else:
            responseObject = {
            'status': 'fail',
            'message': 'Email doesnot exist'
            }

            return make_response(jsonify(responseObject), 202)

    except SignatureExpired:
        responseObject = {
            'status': 'fail',
            'message': 'The token has expired'
        }

        return make_response(jsonify(responseObject), 202)
    except BadSignature:
        responseObject = {
            'status': 'fail',
            'message': 'Invalid Token'
        }

        return make_response(jsonify(responseObject), 402)

@api.route('/login', methods=['POST'])
def login():
    auth = request.form

    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!!"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!!"'})

    if bcrypt.check_password_hash(user.password, auth.get('password')):
        if not user.confirmed:
            return make_response(jsonify({
                'status': 'fail',
                'message': 'Confirm your email first to gain access.'
            }))

        token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!!"'})