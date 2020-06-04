from flask import request,make_response, jsonify, url_for
import uuid, jwt, datetime
from functools import wraps
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

from api import app, bcrypt
from api.routes import api
from api.models import db
from api.models.users import User
from api.email.tasks import deliver_email


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

# signup route
@api.route('/signup', methods=['POST'])
def signup():
    """User Signup

    POST DATA:
    name : Name of the User
    email : Email of the User
    password : Password of the user

    Returns:
        201 -- success
        202 -- fail (user already exists)
        401 -- fail (unknown error)
    """
    data = request.form

    name, email, password = data.get('name'), data.get('email'), data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        try:
            # token
            token = urlsafe.dumps(email, salt='email-confirm')
            # email queue
            deliver_email.delay(
                template='confirmation.html',
                subject='IMPORTANT: EMAIL CONFIRMATION',
                name=name,
                email=email,
                link=f"{app.config['PUBLIC_DOMAIN']}/api/confirm/{token}"
            )
            # database ORM object
            user = User(
                name=name,
                email=email,
                password=password
            )
            # insert user
            db.session.add(user)
            db.session.commit()

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

# verification of token for email confirmation
@api.route('/confirm/<token>', methods=['GET'])
def confirm(token):
    """Email Confirmation (dynamic url)

    GET

    Returns:
        201 -- success
        202 -- fail (email does not exists)
        402 -- fail (token expired / bad signature) note: read from responseObject message
    """
    try:
        email = urlsafe.loads(token, salt='email-confirm', max_age=3600)
        user = User.query.filter_by(email=email).first()

        if user:
            user.confirmed=True
            # commiting changes to db
            db.session.commit()

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
            'message': 'The token has expired!! Please generate a new token'
        }

        return make_response(jsonify(responseObject), 402)
    except BadSignature:
        responseObject = {
            'status': 'fail',
            'message': 'Invalid Token'
        }

        return make_response(jsonify(responseObject), 402)

# forgot password
@api.route('/forgotpassword', methods=['POST'])
def forgotpassword():
    """Forgot Password

    POST Data:
    email : user email

    Returns:
        201 -- success (confirmation mail sent)
        401 -- fail (either email or password is incorrect)
        402 -- fail (unknown error. Try again!)
        403 -- fail (user does not exist)
    """
    email = request.form.get('email')

    user = User.query.filter_by(email=email).first()

    if not user:
        responseObject = {
            'status': 'fail',
            'message': 'Email doesnot exist!'
        }
        return make_response(jsonify(responseObject), 403)

    try:
        name = user.name
        # token
        token = urlsafe.dumps(email, salt='password-reset')
        # email queue
        deliver_email.delay(
            template='reset.html',
            subject='IMPORTANT: Password Reset',
            name=name,
            email=email,
            link=f"http://localhost:5000/api/reset/{token}"
        )

        responseObject = {
            'status': 'success',
            'message': 'Email successfully sent'
        }

        return make_response(jsonify(responseObject), 201)
    except Exception:
        responseObject = {
            'status': 'fail',
            'message': 'Some error occured!! Try again!!'
        }
        return make_response(jsonify(responseObject), 402)

# verification of token for forgot password option
@api.route('/reset/<token>', methods=['PUT'])
def forgotpassword_reset(token):
    """Password Reset (dynamic url)

    PUT Data:
    email : user email
    password : new password of the user

    Returns:
        201 -- success
        202 -- fail (email does not exists)
        402 -- fail (token expired / bad signature) note: read from responseObject message
    """
    try:
        email = urlsafe.loads(token, salt='password-reset', max_age=3600)
        user = User.query.filter_by(email=email).first()

        if user:

            password = request.form.get('password')
            # salting and hashing password
            user.password = bcrypt.generate_password_hash(
                password, app.config.get('BCRYPT_LOG_ROUNDS')
            ).decode()
            # commiting changes to db
            db.session.commit()

            responseObject = {
                'status': 'success',
                'message': 'Password successfully changed'
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
            'message': 'The token has expired!! Please try again my reseting your password'
        }

        return make_response(jsonify(responseObject), 402)
    except BadSignature:
        responseObject = {
            'status': 'fail',
            'message': 'Invalid Token'
        }

        return make_response(jsonify(responseObject), 402)

@api.route('/login', methods=['POST'])
def login():
    """Login

    POST Data:
    email : user email
    password : new password of the user

    Returns:
        201 -- success
        401 -- fail (either email or password is incorrect)
        402 -- fail (user not confirmed)
        403 -- forbidden (user banned)
    """
    auth = request.form

    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!!"'})

    user = User.query.filter_by(email=auth.get('email')).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!!"'})

    if bcrypt.check_password_hash(user.password, auth.get('password')):
        if not user.confirmed:
            return make_response(jsonify({
                'status': 'fail',
                'message': 'Confirm your email!!'
            }), 402)
        if user.BANNED:
            return make_response({
                'status' : 'fail',
                'message': 'USER BANNED!!'
            }, 403)

        token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!!"'})