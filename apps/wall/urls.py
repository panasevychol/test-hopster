import webapp2

from views import MainHandler

urls = [
    webapp2.Route('/', MainHandler),
]
