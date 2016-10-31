import os

import webapp2
import jinja2

from google.appengine.api import mail
from webapp2_extras import sessions

from config import SECRET_KEY

from constants import WRITINGS_PER_PAGE
from utils import get_page_quantity, request_api


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class WallRequestHandler(webapp2.RequestHandler):

    SESSION_EXPIRED_ERROR = 'Session expired. Please re-login.'

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

    def init_login(self, error=None):
        template_values = {}
        if error:
            template_values['error'] = error
        self.response.write(JINJA_ENVIRONMENT.get_template('login.html').render(
            template_values))

    @property
    def current_user_nickname(self):
        return self.session.get('user', {}).get('nickname')

    @property
    def auth_data(self):
        user = self.session.get('user', {})
        return str({
            'token': user.get('token'),
            'email': user.get('email')
        })

    @property
    def is_authorized(self):
        return bool(self.session.get('user'))


class MainHandler(WallRequestHandler):

    def request_wall_api(self, body, method_name):
        body['auth_data'] = self.auth_data
        try:
            return request_api(api_name='wall', method_name=method_name,
                           root_path=self.request.host_url, body=body)
        except Exception as e:
            if not 'Invalid token' in str(e):
                raise e


    def get(self):
        if not self.is_authorized:
            self.init_login()
            return

        add_author_filter, remove_author_filter = (self.request.get('add_author_filter'),
                                                   self.request.get('remove_author_filter'))
        if add_author_filter:
            self.session['filter_author_name'] = add_author_filter
        elif remove_author_filter:
            self.session['filter_author_name'] = None

        filter_author_name = self.session.get('filter_author_name')

        page_number = self.request.get('page_number', 1)

        api_response = self.request_wall_api(body={
            'author_name': filter_author_name,
            'limit': WRITINGS_PER_PAGE,
            'offset': int(page_number)*WRITINGS_PER_PAGE-WRITINGS_PER_PAGE
        }, method_name='list')

        if not api_response:
            self.init_login(error=self.SESSION_EXPIRED_ERROR)
            return

        writings, writings_count = (api_response.get('items', {}),
                                    int(api_response['writings_count']))
        template_values = {
            'writings': writings,
            'page_quantity': get_page_quantity(writings_count),
            'current_page': page_number,
            'logout_url': '/logout',
            'nickname': self.current_user_nickname
        }
        if filter_author_name:
            template_values['filter_author_name'] = filter_author_name
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

    def post(self):
        if not self.is_authorized:
            self.init_login()
            return

        api_response = self.request_wall_api(body={
            'author_name': self.current_user_nickname,
            'writing_body': self.request.get('writing_body')
        }, method_name='create')

        if not api_response:
            self.init_login(error=self.SESSION_EXPIRED_ERROR)
            return

        self.redirect('/')

    def delete(self):
        if not self.is_authorized:
            self.init_login()
            return

        api_response = self.request_wall_api(body={
            'writing_key': self.request.get('writing_key')
        }, method_name='delete')

        if not api_response:
            self.init_login(error=self.SESSION_EXPIRED_ERROR)
            return

        self.redirect('/')


class LoginHandler(WallRequestHandler):

    def request_api_login(self, body):
        return request_api(api_name='users', method_name='login',
                           root_path=self.request.host_url, body=body)

    def login(self, email, nickname, token):
        self.session['user'] = {
            'nickname': nickname,
            'email': email,
            'token': token
        }
        self.redirect('/')

    def logout(self):
        self.session.pop('user')
        self.redirect('/')

    def post(self):
        email, password = self.request.get('email'), self.request.get('password')
        response = self.request_api_login({
            'email': email,
            'password': password
        })
        error, nickname, token = (response.get('error'),
                                  response.get('nickname'),
                                  response.get('token'))
        if error:
            self.init_login(error=error)
        else:
            self.login(email, nickname, token)


class LogoutHandler(WallRequestHandler):

    def get(self):
        self.session.pop('user')
        self.redirect('/')
