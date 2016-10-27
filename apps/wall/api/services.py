import endpoints
# import jwt

from protorpc import message_types, remote, messages
from google.appengine.ext import ndb

from auth_config import (ALLOWED_CLIENT_IDS, ANDROID_AUDIENCE, ANDROID_CLIENT_ID,
                         IOS_CLIENT_ID, WEB_CLIENT_ID)
from messages import (WritingMessage, WritingCollection, UserLoginMessage,
                      SuccessMessage)
from models import Writing, Author, User


@endpoints.api(name='users', version='v1',
               allowed_client_ids=ALLOWED_CLIENT_IDS,
               audiences=[ANDROID_AUDIENCE])
class UsersApi(remote.Service):

    LOGIN_RESOURCE = endpoints.ResourceContainer(
        UserLoginMessage,
        email=messages.StringField(1),
        password=messages.StringField(2))

    @endpoints.method(
        LOGIN_RESOURCE,
        UserLoginMessage,
        path='users',
        http_method='POST',
        name='users.login')
    def login(self, request):
        user = User.query(User.email==request.email).get()
        if not user:
            user = User(email=request.email, password=request.password)
            user.put()
        else:
            if not user.password == request.password:
                return UserLoginMessage(error='Wrong password')
        return UserLoginMessage(nickname=user.nickname())


@endpoints.api(name='wall', version='v1')
class WritingApi(remote.Service):


    CREATE_RESOURCE = endpoints.ResourceContainer(
        SuccessMessage,
        author_name=messages.StringField(1),
        writing_body=messages.StringField(2))

    @endpoints.method(
        CREATE_RESOURCE,
        SuccessMessage,
        path='writings/create',
        http_method='post',
        name='writings.create')
    def create(self, request):
        new_writing = Writing(body=request.writing_body,
                              author=Author(name=request.author_name))
        new_writing.put()
        return SuccessMessage()

    DELETE_RESOURCE = endpoints.ResourceContainer(
        SuccessMessage,
        writing_key=messages.StringField(1))

    @endpoints.method(
        DELETE_RESOURCE,
        SuccessMessage,
        path='writings/delete',
        http_method='post',
        name='writings.delete')
    def delete(self, request):
        key = ndb.Key(urlsafe=request.writing_key)
        key.delete()
        return SuccessMessage(success=True)

    LIST_RESOURCE = endpoints.ResourceContainer(
        WritingCollection,
        author_name=messages.StringField(1),
        limit=messages.IntegerField(2),
        offset=messages.IntegerField(3))

    @endpoints.method(
        LIST_RESOURCE,
        WritingCollection,
        path='writings',
        http_method='post',
        name='writings.list')
    def list_writings(self, request):
        limit, offset = request.limit, request.offset
        if request.author_name:
            writing_query = Writing.query(Writing.author.name==request.author_name)
        else:
            writing_query = Writing.query()

        writings_objects = writing_query.order(-Writing.date).fetch(limit=limit,
                                                                    offset=offset)
        writings = []
        for writing in writings_objects:
            writings.append({
                'body': writing.body,
                'author_name': writing.author.name,
                'date': writing.date,
                'key': writing.key.urlsafe()
            })
        return WritingCollection(items=[ WritingMessage(**writing)
                                        for writing in writings ],
                                 writings_count=writing_query.count())
