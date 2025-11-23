# chats/permissions.py

from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access the API
    - Only participants of a conversation can view/send/update/delete messages
    """

    def has_object_permission(self, request, view, obj):
        # First, ensure user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # obj can be a Conversation or a Message
        conversation = getattr(obj, "conversation", obj)

        # Only allow participants
        if request.user in conversation.participants.all():
            return True

        # Explicitly deny unsafe HTTP methods
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return False

        # Allow read-only methods if participant
        return request.method in permissions.SAFE_METHODS
