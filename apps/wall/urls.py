import webapp2

from views import MainHandler, LoginHandler, LogoutHandler

urls = [
    webapp2.Route('/', MainHandler),
    webapp2.Route('/login', LoginHandler),
    webapp2.Route('/logout', LogoutHandler)

]
