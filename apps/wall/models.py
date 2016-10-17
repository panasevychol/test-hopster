from google.appengine.ext import ndb


class Author(ndb.Model):
    """Sub model for representing an author."""
    name = ndb.StringProperty(required=True)

class Writing(ndb.Model):
    """A model to represent a Writing."""
    author = ndb.StructuredProperty(Author)
    body = ndb.StringProperty(indexed=False, required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
