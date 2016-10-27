import endpoints

from protorpc import message_types, remote, messages
from google.appengine.ext import ndb

from messages import (WritingMessage, WritingCollection, UserLoginMessage,
                      SuccessMessage)
from models import Writing, Author, User
from utils import get_token, authenticate


@endpoints.api(name='users', version='v1')
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
        return UserLoginMessage(email=user.email,
                                nickname = user.nickname(),
                                token=get_token(user.email))


@endpoints.api(name='wall', version='v1')
class WritingApi(remote.Service):


    CREATE_RESOURCE = endpoints.ResourceContainer(
        SuccessMessage,
        auth_data=messages.StringField(1),
        author_name=messages.StringField(2),
        writing_body=messages.StringField(3))

    @endpoints.method(
        CREATE_RESOURCE,
        SuccessMessage,
        path='writings/create',
        http_method='post',
        name='writings.create')
    def create(self, request):
        authenticate(request)
        new_writing = Writing(body=request.writing_body,
                              author=Author(name=request.author_name))
        new_writing.put()
        return SuccessMessage(success=True)


    DELETE_RESOURCE = endpoints.ResourceContainer(
        SuccessMessage,
        auth_data=messages.StringField(1),
        writing_key=messages.StringField(2))

    @endpoints.method(
        DELETE_RESOURCE,
        SuccessMessage,
        path='writings/delete',
        http_method='post',
        name='writings.delete')
    def delete(self, request):
        authenticate(request)
        key = ndb.Key(urlsafe=request.writing_key)
        key.delete()
        return SuccessMessage(success=True)


    LIST_RESOURCE = endpoints.ResourceContainer(
        WritingCollection,
        auth_data=messages.StringField(1),
        author_name=messages.StringField(2),
        limit=messages.IntegerField(3),
        offset=messages.IntegerField(4))

    @endpoints.method(
        LIST_RESOURCE,
        WritingCollection,
        path='writings',
        http_method='post',
        name='writings.list')
    def list_writings(self, request):
        authenticate(request)
        limit, offset = request.limit, request.offset
        if request.author_name:
            writing_query = Writing.query(Writing.author.name
                                          ==str(request.author_name))
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
