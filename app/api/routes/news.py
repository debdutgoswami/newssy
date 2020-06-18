from flask import request, make_response, jsonify

from api import app

from api.routes import api
from api.routes.auth import token_required, urlsafe

from api.models import db
from api.models.users import User
from api.models.news import News

from api.email.tasks import deliver_email

def get_filter_by(category, source, country):
    """For generating suitable function parameters for querying the database

    Args:
        category (list): list of categories
        source (list): list of sources
        country (list): list of sources

    Returns:
        dict: function parameters
    """
    if len(category) and len(source) and len(country):
        return {
            "category": category[0],
            "source": source[0],
            "country": country[0]
        }
    elif len(category) and len(source):
        return {"category": category[0], "source": source[0]}
    elif len(source) and len(country):
        return {"source": source[0], "country": country[0]}
    elif len(country) and len(category):
        return {"category": category[0], "country": country[0]}
    elif len(category):
        return {"category": category[0]}
    elif len(source):
        return {"source": source[0]}
    elif len(country):
        return {"country": country[0]}
    else:
        return dict()


@api.route('/get-news', methods=['POST'])
# @token_required
def get_by_filter():
    """Fetch News

    POST DATA:
    category : filter by category (ARRAY)
    source : filter by source (ARRAY)
    country : filter by country/region (ARRAY)
    page : current page number (default : 1)
    per_page : number of items per page (default : 20)

    Returns:
        201 -- success
        401 -- page not found
    """

    data = request.get_json(silent=True)

    category = data.get('category', list())
    source = data.get('source', list())
    country = data.get('country', list())

    page = data.get('page', 1)
    per_page = data.get('per_page', 20)

    responseARRAY = list()
    try:
        func_parms = get_filter_by(category, source, country)

        # order by latest to oldest
        # per_page will send that many articles in each request
        # page will say which page to traverse
        # `**func_parms` are function parameters passed as dictionary
        articles = News.query.filter_by(
            **func_parms
        ).order_by(News.lastupdated.desc())\
        .paginate(page=page, per_page=per_page)

        for article in articles.items:
            responseARRAY.append({
                'public_id': article.public_id,
                'country': article.country,
                'title': article.title,
                'url': article.url,
                'source': article.source,
                'time': article.lastupdated,
                'category': article.category
            })

        return make_response({
            'status' : 'success',
            'message': responseARRAY
        }, 201)
    except:
        return make_response({
            'status' : 'fail',
            'message': 'Page not found'
        })
