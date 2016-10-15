import webapp2
from blog.urls import urls

app = webapp2.WSGIApplication(urls, debug=True)
