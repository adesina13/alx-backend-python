from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


# ----------------------------------------
# Conversation ViewSet
# ----------------------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.all()

    @action(detail=False, methods=['post'])
    def create_conversation(self, request):
        """
        Create a new conversation with participants.
        """
        user_ids = request.data.get("participants")

        if not user_ids:
            return Response({"error": "Participants list required"}, status=400)

        conversation = Conversation.objects.create()
        conversation.participants.set(User.objects.filter(user_id__in=user_ids))
        conversation.save()

        return Response(ConversationSerializer(conversation).data, status=201)


# ----------------------------------------
# Message ViewSet
# ----------------------------------------
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    @action(detail=False, methods=['post'])
    def send_message(self, request):
        """
        Send a message in a conversation.
        """
        conversation_id = request.data.get("conversation")
        sender_id = request.data.get("sender")
        body = request.data.get("message_body")

        conversation = Conversation.objects.filter(conversation_id=conversation_id).first()
        sender = User.objects.filter(user_id=sender_id).first()

        if not (conversation and sender):
            return Response({"error": "Invalid conversation or sender"}, status=400)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=body
        )

        return Response(MessageSerializer(message).data, status=201)
