import webapp2
from apps.wall.urls import urls

app = webapp2.WSGIApplication(urls, debug=True)
