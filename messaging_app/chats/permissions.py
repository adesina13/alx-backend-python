# chats/permissions.py

from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to view, send, update, or delete messages.
    """

    def has_object_permission(self, request, view, obj):
        # obj can be a Conversation or Message
        conversation = getattr(obj, "conversation", obj)

        # Only participants are allowed
        if request.user in conversation.participants.all():
            return True

        # Explicitly check unsafe HTTP methods
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return False

        # Allow read-only if participant (GET, HEAD, OPTIONS)
        return request.method in permissions.SAFE_METHODS
