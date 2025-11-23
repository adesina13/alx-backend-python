# chats/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import MessagePagination


# ----------------------------------------
# Conversation ViewSet
# ----------------------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    """
    Manage conversations:
    - Only participants can view their conversations
    - Custom action to create a conversation
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Only show conversations where the current user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    @action(detail=False, methods=['post'])
    def create_conversation(self, request):
        """
        Create a new conversation with participants.
        The requesting user is always included automatically.
        """
        user_ids = request.data.get("participants", [])

        if not user_ids:
            return Response({"error": "Participants list required"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure current user is included
        if request.user.id not in user_ids:
            user_ids.append(request.user.id)

        conversation = Conversation.objects.create()
        conversation.participants.set(user_ids)
        conversation.save()

        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)


# ----------------------------------------
# Message ViewSet
# ----------------------------------------
class MessageViewSet(viewsets.ModelViewSet):
    """
    Manage messages:
    - Only participants of a conversation can view/send/update/delete messages
    - Supports filtering and pagination
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = MessagePagination

    def get_queryset(self):
        # Only messages in conversations the user participates in
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get("conversation")
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation")
        serializer.save(sender=self.request.user)

    @action(detail=False, methods=['post'])
    def send_message(self, request):
        """
        Custom action to send a message in a conversation.
        Uses request.user as sender.
        """
        conversation_id = request.data.get("conversation")
        body = request.data.get("message_body")

        if not conversation_id or not body:
            return Response({"error": "Conversation ID and message_body required"},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.filter(id=conversation_id).first()

        if not conversation:
            return Response({"error": "Invalid conversation"}, status=status.HTTP_400_BAD_REQUEST)

        if request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation")

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            message_body=body
        )

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
