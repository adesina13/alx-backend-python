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


# -------------------------------------------------------------------
# Conversation ViewSet
# -------------------------------------------------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    """
    Handles:
    - Listing conversations for the authenticated user
    - Creating new conversations
    - Retrieving, updating, deleting conversations
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Only show conversations where the user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    @action(detail=False, methods=['post'])
    def create_conversation(self, request):
        """
        Custom endpoint:
        Create a new conversation and assign participants.
        The requesting user is ALWAYS automatically included.
        """
        user_ids = request.data.get("participants", [])

        if not isinstance(user_ids, list) or len(user_ids) == 0:
            return Response(
                {"error": "Participants list is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ensure the requesting user is part of the conversation
        if request.user.id not in user_ids:
            user_ids.append(request.user.id)

        conversation = Conversation.objects.create()
        conversation.participants.set(user_ids)
        conversation.save()

        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED
        )


# -------------------------------------------------------------------
# Message ViewSet
# -------------------------------------------------------------------
class MessageViewSet(viewsets.ModelViewSet):
    """
    Handles:
    - Sending messages
    - Listing messages in user conversations
    - Filtering messages by sender/date (via django-filters)
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = MessagePagination

    def get_queryset(self):
        # User can only see messages in conversations they participate in
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        """
        When creating a message using POST /api/messages/,
        ensure the user is a participant of the conversation.
        """
        conversation = serializer.validated_data.get("conversation")

        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer.save(sender=self.request.user)

    @action(detail=False, methods=['post'])
    def send_message(self, request):
        """
        Custom endpoint: POST /api/messages/send_message/
        Use this if you want a manual message send action.
        """
        conversation_id = request.data.get("conversation")
        message_body = request.data.get("message_body")

        if not conversation_id or not message_body:
            return Response(
                {"error": "conversation ID and message_body are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.filter(id=conversation_id).first()
        if not conversation:
            return Response(
                {"error": "Invalid conversation ID"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ensure user belongs to this conversation
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN
            )

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            message_body=message_body
        )

        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )
