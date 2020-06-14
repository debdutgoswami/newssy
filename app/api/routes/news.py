from flask import request, make_response, jsonify

from api import app

from api.routes import api
from api.routes.auth import token_required, urlsafe

from api.models import db
from api.models.users import User
from api.models.news import News

from api.email.tasks import deliver_email

@api.route('/get-news', methods=['POST'])
# @token_required
def get_by_filter():
    """Fetch News

    POST DATA:
    category : filter by category
    source : filter by source
    region : filter by region/country

    Returns:
        201 -- success
        401 -- fail (unknown error)
    """

    data = request.get_json(silent=True)

    category = data.get('category', None)
    source = data.get('source', None)
    region = data.get('region', None)

    start = data.get('start')
    stop = data.get('stop')

    final = list()

    articles = News.query.filter_by(
        category = category
    )

    for article in articles:
        final.append({
            'public_id': article.public_id,
            'country': article.country,
            'title': article.title,
            'url': article.url,
            'body': article.body,
            'source': article.source,
            'category': article.category
        })

    return make_response({
        'status' : 'success',
        'message': final
    }, 201)