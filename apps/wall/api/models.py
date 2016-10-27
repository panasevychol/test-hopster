from google.appengine.ext import ndb


class User(ndb.Model):
    """A model to represent a User."""
    email = ndb.StringProperty(required=True, repeated=False)
    password = ndb.StringProperty(required=True)

    def nickname(self):
        return self.email.split('@')[0]


class Author(ndb.Model):
    """Sub model for representing an author."""
    name = ndb.StringProperty(required=True)


class Writing(ndb.Model):
    """A model to represent a Writing."""
    author = ndb.StructuredProperty(Author)
    body = ndb.StringProperty(indexed=False, required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

    # def short_date(self):
    #     return self.date.strftime("%H:%M   %b %d %Y")
