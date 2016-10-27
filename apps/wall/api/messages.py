from protorpc import messages, message_types

class WritingMessage(messages.Message):
    author_name = messages.StringField(1, required=True)
    body = messages.StringField(2, required=True)
    date = message_types.DateTimeField(3, required=True)
    key = messages.StringField(4, required=True)

class SuccessMessage(messages.Message):
    success = messages.BooleanField(1)

class WritingCollection(messages.Message):
    """Collection of Writings."""
    items = messages.MessageField(WritingMessage, 1, repeated=True)
    writings_count = messages.IntegerField(2)


class UserLoginMessage(messages.Message):
    error = messages.StringField(1)
    nickname = messages.StringField(2)
    token = messages.StringField(3)
    email = messages.StringField(4)
