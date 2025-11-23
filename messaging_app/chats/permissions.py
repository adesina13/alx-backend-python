from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants
    in the conversation or in the related message's conversation.
    """

    def has_permission(self, request, view):
        # Only authenticated users allowed overall
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj can be a Conversation or Message
        if hasattr(obj, "participants"):
            conversation = obj
        else:
            conversation = obj.conversation

        return request.user in conversation.participants.all()
