import endpoints

from apps.wall.api.services import WritingApi, UsersApi

api = endpoints.api_server([WritingApi, UsersApi])
