import os

import webapp2
import jinja2

from google.appengine.api import users

from models import Writing, Author
from constants import WRITINGS_PER_PAGE
from utils import get_page_quantity

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):

    def get(self):
        author_name_to_filter = self.request.get('author_name_to_filter')
        if author_name_to_filter:
            writing_query = Writing.query(Writing.author.name==author_name_to_filter)
        else:
            writing_query = Writing.query()

        page_number = self.request.get('page_number', 1)
        writings = writing_query.order(-Writing.date).fetch(
            limit=WRITINGS_PER_PAGE,
            offset=int(page_number)*WRITINGS_PER_PAGE-WRITINGS_PER_PAGE)

        page_quantity = writing_query.count() / WRITINGS_PER_PAGE
        if writing_query.count() % WRITINGS_PER_PAGE:
            page_quantity += 1

        template_values = {
            'writings': writings,
            'page_quantity': get_page_quantity(writing_query.count()),
            'current_page': page_number
        }

        if author_name_to_filter:
            template_values['author_name_to_filter'] = author_name_to_filter
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

    def post(self):
        writing_body, author_name = self.request.get('writing_body'), self.request.get('author_name')
        if writing_body and author_name:
            new_writing = Writing(body=writing_body,
                                  author=Author(name=author_name))
            new_writing.put()

        writing_to_delete_key = self.request.get('writing_to_delete_key')
        if writing_to_delete_key:
            raise NotImplementedError

        self.redirect('/')


class WritingsHandler(webapp2.RequestHandler):
    def get(self, author_name):
        page_number = self.request.get('page_number', 1)
        writing_query = Writing.query(Writing.author.name==author_name)
        writings = writing_query.order(-Writing.date).fetch(
            limit=WRITINGS_PER_PAGE,
            offset=int(page_number)*WRITINGS_PER_PAGE-WRITINGS_PER_PAGE)

        template_values = {
            'writings': writings,
            'author_name': author_name,
            'current_page': page_number,
            'page_quantity': get_page_quantity(writing_query.count())
        }
        template = JINJA_ENVIRONMENT.get_template('author_writings.html')
        self.response.write(template.render(template_values))
