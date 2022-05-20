import os
import urllib.parse

import requests
from flask import Blueprint, request, redirect, session, url_for, render_template

blueprint = Blueprint('auth', __name__, url_prefix='/auth')

AUTHENTICATION_DOCUMENT_URL = os.environ.get(
    'CM_AUTHENTICATION_DOCUMENT_URL',
    'http://cm.hilbertteam.net/authentication_document')


@blueprint.route('/', methods=('GET',))
def index():
    response = requests.get(AUTHENTICATION_DOCUMENT_URL)
    authentication_document = response.json()

    authentication_documents = authentication_document['authentication']
    result_authentication_documents = []

    for authentication_document in authentication_documents:
        authenticate_links = list(filter(lambda link: link['rel'] == 'authenticate', authentication_document['links']))

        for authenticate_link in authenticate_links:
            result_authentication_document = {
                'display_name': authenticate_link['display_names'][0]['value'] if authenticate_link['display_names'] else '',
                'description': authenticate_link['descriptions'][0]['value'] if authenticate_link['descriptions'] else '',
                'information_url': authenticate_link['information_urls'][0]['value'] if authenticate_link['information_urls'] else '',
                'privacy_statement_url': authenticate_link['privacy_statement_urls'][0]['value'] if authenticate_link['privacy_statement_urls'] else '',
                'logo_url': authenticate_link['logo_urls'][0]['value'] if authenticate_link['logo_urls'] else '',
                'href': requests.utils.quote(authenticate_link['href'])
            }
            result_authentication_documents.append(result_authentication_document)

    return render_template('auth/index.html', authentication_documents=result_authentication_documents)


@blueprint.route('/login', methods=('GET', 'POST',))
def login():
    if 'access_token' in request.args:
        token = request.args.get('access_token')
        session['ACCESS_TOKEN'] = token

        return redirect(url_for('home.index'))
    else:
        authentication_url = requests.utils.unquote(request.args.get('link'))
        redirect_uri = url_for('auth.login', _external=True)

        authentication_url += '&redirect_uri=' + requests.utils.quote(redirect_uri)

        return redirect(authentication_url)


@blueprint.route('/logout', methods=('GET',))
def logout():
    del session['ACCESS_TOKEN']
    return redirect(url_for('home.index'))
