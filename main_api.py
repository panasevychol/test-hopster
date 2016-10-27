"""This is a sample Hello World API implemented using Google Cloud
Endpoints."""

import endpoints

from apps.wall.api.services import WritingApi, UsersApi

api = endpoints.api_server([WritingApi, UsersApi])
