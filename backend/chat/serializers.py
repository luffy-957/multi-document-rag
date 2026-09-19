from rest_framework import serializers

from .models import Conversation, Message

class ConversationListSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = Conversation
        fields = (
            "id",
            "title",
            "created_at",
            "updated_at",
        )
class ChatRequestSerializer(serializers.Serializer):
    question = serializers.CharField(
        max_length=5000,
        allow_blank=False,
    )

    conversation_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )

    document_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        required=False,
        allow_empty=True,
    )

    k = serializers.IntegerField(
        required=False,
        min_value=1,
        max_value=10,
        default=4,
    )


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            "id",
            "role",
            "content",
            "sources",
            "created_at",
        )


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Conversation
        fields = (
            "id",
            "title",
            "messages",
            "created_at",
            "updated_at",
        )