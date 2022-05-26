import os

from urllib.parse import urlparse

from flask import Blueprint, redirect, request, url_for

from flask_sp.saml.auth import AuthenticationManager

blueprint = Blueprint('books', __name__, url_prefix='/books')

IDP_HOSTNAME = os.environ.get('IDP_HOSTNAME', 'idp.hilbertteam.net')
IDP_ENTITYID = os.environ.get('IDP_ENTITYID', 'http://idp.hilbertteam.net/idp/shibboleth')


@blueprint.route('/<book>', methods=('GET',))
def index(book):
    auth_manager = AuthenticationManager(IDP_ENTITYID)

    authentication_manager = AuthenticationManager()

    authenticated = True

    while True:
        if request.referrer:
            parse_result = urlparse(request.referrer)

            if IDP_HOSTNAME in parse_result.netloc:
                break

        user = authentication_manager.finish_authentication()

        if user:
            break

        authenticated = False
        break

    if authenticated:
        return redirect(url_for('static', filename='books/' + book, _external=True))

    return redirect(auth_manager.start_authentication(request.url))


