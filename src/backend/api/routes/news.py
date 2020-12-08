from flask import request, make_response

from .. import app

from ..routes import api
from ..routes.auth import token_required, token_partial_required

from ..models import db
from ..models.news import News



def get_filter_by(category, source, country):
    """For generating suitable function parameters for querying the database

    Args:
        category (list): category
        source (list): source
        country (list): country

    Returns:
        list: arguments
    """
    parms = list()

    if len(category):
        parms.append(News.category.in_(category))
    if len(source):
        parms.append(News.source.in_(source))
    if len(country):
        parms.append(News.country.in_(country))

    return parms


@api.route('/get-news', methods=['POST'])
@token_partial_required
def get_by_filter(current_user):
    """Fetch News

    POST DATA:
    category : filter by category (ARRAY)
    source : filter by source (ARRAY)
    country : filter by country/region (ARRAY)
    page : current page number (default : 1)(INT)
    per_page : number of items per page (default : 20)(INT)

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
        # `*func_parms` are function parameters passed as list of arguments
        if len(func_parms):
            articles = News.query.filter(
                *func_parms
            ).order_by(News.lastupdated.desc()) \
                .paginate(page=page, per_page=per_page)
        else:
            articles = News.query.order_by(News.lastupdated.desc()) \
                .paginate(page=page, per_page=per_page)

        for article in articles.items:
            responseARRAY.append({
                'public_id': article.public_id,
                'country': article.country,
                'title': article.title,
                'body': article.body,
                'url': article.url,
                'img': article.img_url,
                'source': article.source,
                'time': article.lastupdated,
                'category': article.category
            })

        return make_response({
            'status': 'success',
            'articles': responseARRAY
        }, 201)
    except Exception:
        return make_response({
            'status': 'fail',
            'message': 'Page not found'
        }, 204)


@api.route('/add-article', methods=['POST'])
@token_required
def add_article(current_user):
    public_id = request.get_json(silent=True).get('public_id', None)

    if not current_user.saved_article:
        current_user.saved_article = list()
        db.session.commit()

    saved_article = current_user.saved_article

    if public_id in saved_article:
        return make_response({
            'status': 'fail',
            'message': 'Article already saved!'
        }, 202)

    saved_article.append(public_id)
    current_user.saved_article = saved_article
    db.session.commit()

    return make_response({
        "status": "success"
    }, 201)
