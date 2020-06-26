import os

from StringIO import StringIO

import requests
from flask import Blueprint, render_template, session, redirect, url_for
from lxml import etree

blueprint = Blueprint('home', __name__, url_prefix='/')


GROUPS_URL = os.environ.get('CM_GROUPS_URL', 'http://cm.hilbertteam.net/SAML/groups')


@blueprint.route('/', methods=('GET', 'POST',))
def index():
    access_token = session.get('ACCESS_TOKEN')

    if not access_token:
        return redirect(url_for('auth.index'))

    books = []

    if access_token:
        response = requests.get(GROUPS_URL)
        group_feed = StringIO(response.content)
        tree = etree.parse(group_feed)
        namespaces = {"atom": "http://www.w3.org/2005/Atom"}
        entry_nodes = tree.xpath('//atom:entry', namespaces=namespaces)

        for entry_node in entry_nodes:
            title_nodes = entry_node.xpath('./atom:title', namespaces=namespaces)
            title = title_nodes[0].text

            author_nodes = entry_node.xpath('./atom:author/atom:name', namespaces=namespaces)
            author = author_nodes[0].text

            summary_nodes = entry_node.xpath('./atom:summary', namespaces=namespaces)
            summary = summary_nodes[0].text

            borrow_link_nodes = entry_node.xpath(
                './atom:link[@rel="http://opds-spec.org/acquisition/borrow"]', namespaces=namespaces)
            borrow_link = requests.utils.quote(borrow_link_nodes[0].get('href'))

            download_link_nodes = entry_node.xpath(
                './atom:link[@rel="http://opds-spec.org/acquisition/open-access"]', namespaces=namespaces)
            download_link = requests.utils.quote(download_link_nodes[0].get('href'))

            book = {
                'title': title,
                'author': author,
                'summary': summary,
                'borrow_link': borrow_link,
                'download_link': download_link
            }

            books.append(book)

    return render_template('home/index.html', access_token=access_token, books=books)
