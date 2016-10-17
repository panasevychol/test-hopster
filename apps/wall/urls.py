import webapp2

from views import MainHandler, WritingsHandler

urls = [
    webapp2.Route('/', MainHandler),
    webapp2.Route('/writings/<author_name>', WritingsHandler)
]
