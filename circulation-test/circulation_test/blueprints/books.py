import requests
from flask import Blueprint, session, request

blueprint = Blueprint('books', __name__, url_prefix='/books')


@blueprint.route('/borrow', methods=('GET',))
def borrow():
    link = requests.utils.unquote(request.args.get('link'))
    access_token = session['ACCESS_TOKEN']
    book_response = requests.get(
        link,
        headers={'Authorization': f'Bearer: {access_token}'},
        allow_redirects=False)

    return book_response.content, book_response.status_code, book_response.headers.items()


@blueprint.route('/download', methods=('GET',))
def download():
    link = requests.utils.unquote(request.args.get('link'))
    access_token = session['ACCESS_TOKEN']
    book_response = requests.get(
        link,
        headers={'Authorization': f'Bearer: {access_token}'},
        allow_redirects=False)

    return book_response.content, book_response.status_code, book_response.headers.items()

