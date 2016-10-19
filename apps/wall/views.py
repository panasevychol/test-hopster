import os

import webapp2
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import sessions

from models import Writing, Author
from constants import WRITINGS_PER_PAGE
from utils import get_page_quantity

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):

    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url())
            return

        add_author_filter, remove_author_filter = (self.request.get('add_author_filter'),
                                                   self.request.get('remove_author_filter'))
        if add_author_filter:
            self.session['filter_author_name'] = add_author_filter
        elif remove_author_filter:
            self.session['filter_author_name'] = None

        filter_author_name = self.session.get('filter_author_name')
        if filter_author_name:
            writing_query = Writing.query(Writing.author.name==filter_author_name)
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
            'current_page': page_number,
            'logout_url': users.create_logout_url('/'),
            'nickname': user.nickname()
        }
        if filter_author_name:
            template_values['filter_author_name'] = filter_author_name
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url())
            return

        writing_body, author_name = self.request.get('writing_body'), self.request.get('author_name')
        print writing_body, author_name
        if writing_body and author_name:
            new_writing = Writing(body=writing_body,
                                  author=Author(name=author_name))
            new_writing.put()

        self.redirect('/')

    def delete(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url())
            return

        ndb.Key(urlsafe=self.request.get('writing_key')).delete()
