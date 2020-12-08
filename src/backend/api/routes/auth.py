from functools import wraps
import datetime
import jwt
from flask import request, make_response, jsonify
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from .. import app, bcrypt
from ..email.tasks import deliver_email
from ..models import db
from ..models.users import User
from ..routes import api

urlsafe = URLSafeTimedSerializer(app.config.get("SECRET_KEY"))


# checking whether loged-in or not based on that info, data is provided
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        """
        Not checking whether the user has confirmed the email because
        access token won't be issued if the user is not verified.
        """

        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return jsonify({"message": "Token is missing!!"}), 401

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = User.query.filter_by(public_id=data["public_id"]).first()
        except:
            return jsonify({"message": "Token is invalid!!"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


# partially protecting news route so that
# only authenticated users can access
# page more than 1 or per page articles more than 20
def token_partial_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        """
        Not checking whether the user has confirmed the email because
        access token won't be issued if the user is not verified.
        """

        token = None
        data = request.get_json(silent=True)
        page = data.get("page", 1)
        per_page = data.get("per_page", 20)

        if "x-access-token" in request.headers:
            token = request.headers.get("x-access-token")

        if not token and (page > 1 or per_page > 20):
            # Checks if user is requesting for any page other than first page or
            # whether the user is requesting for more than 20 articles in a single page

            return jsonify({"message": "Token is missing!!"}), 401

        try:
            if not token:
                current_user = None
            else:
                data = jwt.decode(token, app.config["SECRET_KEY"])
                current_user = User.query.filter_by(public_id=data.get("public_id")).first()
        except:
            return jsonify({"message": "Token is invalid!!"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


def send_confirmation_token(email: str, name: str):
    # token
    token = urlsafe.dumps(email, salt="email-confirm")
    # email queue
    deliver_email(
        template="confirmation.html",
        subject="IMPORTANT: EMAIL CONFIRMATION",
        name=name,
        email=email,
        link=f"http://{app.config['PUBLIC_DOMAIN']}/confirm?token={token}",
    )


# signup route
@api.route("/signup", methods=["POST"])
def signup():
    """User Signup

    POST DATA:
    fname : First Name of the User
    lname : Last Name of the User
    email : Email of the User
    password : Password of the user

    Returns:
        201 -- success
        202 -- fail (user already exists)
        401 -- fail (unknown error)
    """
    data = request.get_json(silent=True)

    fname, lname, email, password = (
        data.get("fname"),
        data.get("lname"),
        data.get("email"),
        data.get("password"),
    )

    user = User.query.filter_by(email=email).first()

    if not user:
        try:
            # send confirmation email
            send_confirmation_token(email, fname)
            # database ORM object
            user = User(
                first_name=fname, last_name=lname, email=email, password=password
            )
            # insert user
            db.session.add(user)
            db.session.commit()

            responseObject = {
                "status": "success",
                "message": "Successfully registered. Kindly check your mail!!",
            }

            return make_response(jsonify(responseObject), 201)
        except Exception:
            responseObject = {
                "satus": "fail",
                "message": "Some error occured. Please try again.",
            }

            return make_response(jsonify(responseObject), 401)
    else:
        responseObject = {
            "status": "fail",
            "message": "User already exists. Please Log in.",
        }

        return make_response(jsonify(responseObject), 202)


# resend confirmation email
@api.route("/sendconfirmation", methods=["POST"])
def resend_confirmation():
    """Resend Confirmation
    
    POST

    BODY:
        email -- email to send confirmation token

    Returns:
        201 -- success
        202 -- fail
        502 -- some error occured
    """
    email = request.get_json(silent=True).get("email")
    user = User.query.filter_by(email=email).first()

    if not user:
        return make_response({"status": "fail", "message": "User does not exist"}, 202)

    try:

        send_confirmation_token(email, user.fname)

        return make_response({"status": "success", "message": "Check your email"}, 201)
    except:
        return make_response(
            {"status": "fail", "message": "Some error occured. Try again!!"}, 502
        )


# verification of token for email confirmation
@api.route("/confirm", methods=["POST"])
def confirm():
    """Email Confirmation (dynamic url)

    POST

    Returns:
        201 -- success
        202 -- fail (email does not exists)
        203 -- fail (user already confirmed)
        402 -- fail (token expired / bad signature) note: read from responseObject message
    """

    token = request.get_json(silent=True).get("token", None)

    try:
        email = urlsafe.loads(token, salt="email-confirm", max_age=3600)
        user = User.query.filter_by(email=email).first()

        if user and not user.confirmed:
            user.confirmed = True
            # commiting changes to db
            db.session.commit()

            responseObject = {
                "status": "success",
                "message": "Email successfully confirmed",
            }

            return make_response(jsonify(responseObject), 201)

        elif user.confirmed:
            responseObject = {"status": "fail", "message": "User already confirmed"}
            return make_response(responseObject, 203)

        else:
            responseObject = {"status": "fail", "message": "Email doesnot exist"}

            return make_response(jsonify(responseObject), 202)

    except SignatureExpired:
        responseObject = {
            "status": "fail",
            "message": "The token has expired!! Please generate a new token",
        }

        return make_response(jsonify(responseObject), 402)
    except BadSignature:
        responseObject = {"status": "fail", "message": "Invalid Token"}

        return make_response(jsonify(responseObject), 402)


# forgot password
@api.route("/forgotpassword", methods=["POST"])
def forgotpassword():
    """Forgot Password

    POST Data:
    email : user email

    Returns:
        201 -- success (confirmation mail sent)
        402 -- fail (unknown error. Try again!)
        403 -- fail (user does not exist)
    """
    email = request.get_json(silent=True).get("email")

    user = User.query.filter_by(email=email).first()

    if not user:
        responseObject = {"status": "fail", "message": "Email doesnot exist!"}
        return make_response(jsonify(responseObject), 403)

    try:
        name = user.first_name
        # token
        token = urlsafe.dumps(email, salt="password-reset")
        # email queue
        deliver_email(
            template="reset.html",
            subject="IMPORTANT: Password Reset",
            name=name,
            email=email,
            link=f"http://{app.config['PUBLIC_DOMAIN']}/api/reset/{token}",
        )

        responseObject = {"status": "success", "message": "Email successfully sent"}

        return make_response(jsonify(responseObject), 201)
    except Exception:
        responseObject = {
            "status": "fail",
            "message": "Some error occured!! Try again!!",
        }
        return make_response(jsonify(responseObject), 402)


# verification of token for forgot password option
@api.route("/reset/<token>", methods=["PUT"])
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
        email = urlsafe.loads(token, salt="password-reset", max_age=3600)
        user = User.query.filter_by(email=email).first()

        if user:

            password = request.get_json(silent=True).get("password")
            # salting and hashing password
            user.password = bcrypt.generate_password_hash(
                password, app.config.get("BCRYPT_LOG_ROUNDS")
            ).decode()
            # commiting changes to db
            db.session.commit()

            responseObject = {
                "status": "success",
                "message": "Password successfully changed",
            }

            return make_response(jsonify(responseObject), 201)

        else:
            responseObject = {"status": "fail", "message": "Email doesnot exist"}

            return make_response(jsonify(responseObject), 202)

    except SignatureExpired:
        responseObject = {
            "status": "fail",
            "message": "The token has expired!! Please try again my reseting your password",
        }

        return make_response(jsonify(responseObject), 402)
    except BadSignature:
        responseObject = {"status": "fail", "message": "Invalid Token"}

        return make_response(jsonify(responseObject), 402)


@api.route("/login", methods=["POST"])
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
    auth = request.get_json(silent=True)

    if not auth or not auth.get("email") or not auth.get("password"):
        return make_response("Could not verify", 401)

    user = User.query.filter_by(email=auth.get("email")).first()

    if not user:
        return make_response("Could not verify", 401)

    if bcrypt.check_password_hash(user.password, auth.get("password")):
        if not user.confirmed:
            return make_response(
                jsonify({"status": "fail", "message": "Confirm your email!!"}), 402
            )
        if user.BANNED:
            return make_response({"status": "fail", "message": "USER BANNED!!"}, 403)

        token = jwt.encode(
            {
                "public_id": user.public_id,
                "name": user.first_name,
                "email": user.email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            app.config["SECRET_KEY"],
        )

        return make_response({"token": token.decode("UTF-8")}, 201)

    return make_response("Could not verify", 401)
