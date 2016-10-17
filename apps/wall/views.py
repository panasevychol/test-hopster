import os

import webapp2
import jinja2

from google.appengine.api import users

from models import Writing, Author
from constants import WRITINGS_PER_PAGE

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        page_number = self.request.get('page_number', 1)
        writing_query = Writing.query()
        writings = writing_query.order(-Writing.date).fetch(
            limit=WRITINGS_PER_PAGE,
            offset=int(page_number)*WRITINGS_PER_PAGE-WRITINGS_PER_PAGE)

        page_quantity = writing_query.count() / WRITINGS_PER_PAGE
        if writing_query.count() % WRITINGS_PER_PAGE:
            page_quantity += 1

        template_values = {
            'writings': writings,
            'page_quantity': page_quantity,
            'current_page': page_number
        }
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
        writings = Writing.query(Writing.author.name==author_name).order(-Writing.date).fetch(
            limit=WRITINGS_PER_PAGE,
            offset=int(page_number)*WRITINGS_PER_PAGE-WRITINGS_PER_PAGE)

        template_values = {
            'writings': writings
        }
        template = JINJA_ENVIRONMENT.get_template('author_writings.html')
        self.response.write(template.render(template_values))
