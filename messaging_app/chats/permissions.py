from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Only authenticated users who are participants in the conversation
    can access/modify messages.
    """

    def has_object_permission(self, request, view, obj):
        # obj can be a Conversation or a Message
        conversation = getattr(obj, "conversation", obj)

        return request.user in conversation.participants.all()
