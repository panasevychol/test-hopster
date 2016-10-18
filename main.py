import webapp2

import config

from apps.wall.urls import urls

app = webapp2.WSGIApplication(urls, debug=True, config=config.config)
