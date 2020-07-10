from flask import request, make_response, jsonify

from api import app

from api.routes import api
from api.routes.auth import token_required, urlsafe

from api.models import db
from api.models.users import User
from api.models.news import News, _NEWS_SOURCE

from api.email.tasks import deliver_email

@api.route('/profile-data')
@token_required
def profile_data(current_user):
    """Profile Data

    Request Type:
        GET

    HEADERS:
        x-access-token -- JWT

    Returns:
        responseObject -- profile data

    Response Code:
        201 -- success
    """
    articles = current_user.saved_article

    if articles:
        saved_articles = News.query.filter(
            News.public_id.in_(articles)
        ).all()

        articles = list()

        for article in saved_articles:
            articles.append({
                "title" : article.title, 
                "url" : article.url
            })
        

    responseObject = {
        'first_name'    : current_user.first_name,
        'last_name'     : current_user.last_name,
        'email'         : current_user.email,
        'joined_on'     : current_user.joined_on,
        'preferences'   : current_user.preferences,
        'saved_article' : articles,
        'email_notify'  : current_user.email_notify,
        'verified'      : current_user.VERIFIED
    }

    return make_response(jsonify(responseObject), 201)

@api.route('/change-name', methods=['PUT'])
@token_required
def change_name(current_user):
    """Change Name

    Request Type:
        PUT

    HEADERS:
        x-access-token -- JWT

    BODY:
        first_name -- new first name
        last_name -- new last name

    Returns:
        responseObject -- success or failure

    Response Code:
        201 -- success
        403 -- forbidden
    """
    pass

@api.route('/change-preference', methods=['PUT'])
@token_required
def change_preference(current_user):
    """Change Preferences

    Request Type:
        PUT

    HEADERS:
        x-access-token -- JWT

    BOODY:
        preference -- list of prefered news vendors

    Returns:
        responseObject -- success or failure

    Response Code:
        201 -- success
        401 -- failure
    """

    preferences = list(request.get_json(silent=True).get('preference'))
    try:
        # if not current_user.preferences:
        #     current_user.saved_article = list()
        #     db.session.commit()

        current_user.preferences = preferences
        db.session.commit()

        responseObject = {
            'status' : 'success',
            'message': 'Successfully changed the preferences'
        }

        return make_response(jsonify(responseObject), 201)
    except Exception:
        responseObject = {
            'status' : 'fail',
            'message': 'Some error occured. Try Again!!'
        }

        return make_response(jsonify(responseObject), 401)

@api.route('/email-notification', methods=['PUT'])
@token_required
def email_notification(current_user):
    """Email Notification

    Request Type:
        PUT

    HEADERS:
        x-access-token -- JWT

    BODY:
        email_notify -- Boolean

    Returns:
        responseObject -- success

    Response Code:
        201 -- success
    """
    email_notify = request.get_json(silent=True).get('email_notify')
    current_user.email_notify = email_notify
    db.session.commit()

    responseObject = {
        'status' : 'success',
        'message': 'failure'
    }

    return  make_response(jsonify(responseObject), 201)


@api.route('/change-email', methods=['PUT'])
@token_required
def change_email(current_user):
    """Change Email

    Request Type:
        PUT

    HEADERS:
        x-access-token -- JWT

    BODY:
        email -- new email

    Returns:
        responseObject -- success or failure

    Response Code:
        201 -- success
        401 -- failure (same email)
        402 -- failure (email already exists)
        405 -- Unknown ERROR

    ACTION:
        Destroy the JWT / logout the current user
    """
    email = request.get_json(silent=True).get('email')
    if email == current_user.email:
        responseObject = {
            'status' : 'failure',
            'message': 'New email same as Current email!'
        }

        return make_response(jsonify(responseObject), 401)

    user = User.query.filter_by(email=email).first()

    if user:
        responseObject = {
            'status' : 'failure',
            'message': 'Email Already Exists!'
        }

        return make_response(jsonify(responseObject), 402)
    
    try:
        # token
        token = urlsafe.dumps(email, salt='email-confirm')
        # email queue
        deliver_email.delay(
            template='confirmation.html',
            subject='IMPORTANT: EMAIL CONFIRMATION',
            name=current_user.first_name,
            email=email,
            link=f"{app.config['PUBLIC_DOMAIN']}/confirm?token={token}"
        )
        # insert user
        current_user.email = email
        current_user.confirmed = False
        db.session.commit()

        responseObject = {
            'status': 'success',
            'message': 'Confirm your email!'
        }

        return make_response(jsonify(responseObject), 201)
    except Exception:
        responseObject = {
            'satus': 'fail',
            'message': 'Some error occured. Please try again!'
        }

        return make_response(jsonify(responseObject), 405)

@api.route('/show-saved-article')
@token_required
def saved_article(current_user):
    """Profile Data

    Request Type:
        GET

    HEADERS:
        x-access-token -- JWT

    Returns:
        responseObject -- profile data

    Response Code:
        201 -- success
    """
    articles  = current_user.saved_article

    if not articles:
        responseObject = {
            'status' : 'success',
            'message': {
                'articles' : list() 
            }
        }
    else:
        final = list()
        for pid in articles:
            article = News.query.filter_by(public_id=pid).first()
            final.append({
                'public_id' : article.public_id,
                'title'     : article.title,
                'source'    : article.source,
                'category'  : article.category,
                'country'   : article.country
            })

        responseObject = {
            'status' : 'success',
            'message' : {
                'articles' : final
            }
        }

    return make_response(jsonify(responseObject), 201)


# works for both admin as well as users
@api.route('/admin/scrapers')
@api.route('/list-scrapers')
@token_required
def admin_scrapers(current_user):
    """Scraper List

    Request Type:
        GET

    HEADERS:
        x-access-token -- JWT

    Returns:
        responseObject -- success (list of scrappers)

    Response Code:
        201 -- success
    """

    return make_response({
        'status' : 'success',
        'message': _NEWS_SOURCE
    }, 201)