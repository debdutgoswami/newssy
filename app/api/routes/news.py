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
        category (str): category
        source (str): source
        country (str): country

    Returns:
        dict: function parameters
    """
    if category and source and country:
        return {
            "category": category,
            "source": source,
            "country": country
        }
    elif category and source:
        return {"category": category, "source": source}
    elif source and country:
        return {"source": source, "country": country}
    elif country and category:
        return {"category": category, "country": country}
    elif category:
        return {"category": category}
    elif source:
        return {"source": source}
    elif country:
        return {"country": country}
    else:
        return dict()


@api.route('/get-news', methods=['POST'])
# @token_required
def get_by_filter():
    """Fetch News

    POST DATA:
    category : filter by category (str)
    source : filter by source (str)
    country : filter by country/region (str)
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
