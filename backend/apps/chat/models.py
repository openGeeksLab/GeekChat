import json

from django.contrib.auth import get_user_model
from django.db import models

from channels import Group


User = get_user_model()


class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)

    def __str__(self):
        return 'Room - {}.'.format(self.label)

    @property
    def websocket_group(self):
        """
        Returns the Channels Group that sockets should subscribe to to get messages.
        """
        return Group('chat-{}'.format(self.label))


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages')
    user = models.ForeignKey(User)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '[{timestamp}] {user}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')

    def as_dict(self):
        return {'user': self.user, 'message': self.message, 'timestamp': self.formatted_timestamp}


class UserRoom(models.Model):
    user = models.ForeignKey(User)
    room = models.ForeignKey(Room)

    class Meta:
        unique_together = ('user', 'room')

    def __str__(self):
        return '{} - {}'.format(self.user, self.room)
