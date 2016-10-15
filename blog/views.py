import os

import webapp2
import jinja2

from models import Entry, Author

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        entries = Entry.query().order(-Entry.date).fetch(10)
        template_values = {
            'user': 'aaron',
            'entries': entries
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

        # self.response.write('Hello world!')

    def post(self):
        new_entry = Entry(body=self.request.get('entry_body'),
                          author=Author(name=self.request.get('author_name')))
        new_entry.put()
        self.redirect('/')
