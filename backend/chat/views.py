from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rag.services.rag_service import RAGService

from .models import Conversation, Message
from .serializers import (
    ChatRequestSerializer,
    ConversationSerializer,
)


class ChatView(APIView):

    def post(self, request):
        # --------------------------------------------------
        # Validate request
        # --------------------------------------------------

        serializer = ChatRequestSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        question = serializer.validated_data[
            "question"
        ]

        conversation_id = serializer.validated_data.get(
            "conversation_id"
        )

        document_ids = serializer.validated_data.get(
            "document_ids"
        )

        k = serializer.validated_data.get(
            "k",
            4,
        )

        # --------------------------------------------------
        # Get or create conversation
        # --------------------------------------------------

        if conversation_id is not None:
            try:
                conversation = Conversation.objects.get(
                    id=conversation_id
                )

            except Conversation.DoesNotExist:
                return Response(
                    {
                        "error": (
                            "Conversation not found."
                        )
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

        else:
            conversation = Conversation.objects.create(
                title=question[:80],
            )

        # --------------------------------------------------
        # Save user message
        # --------------------------------------------------

        Message.objects.create(
            conversation=conversation,
            role=Message.Role.USER,
            content=question,
        )

        # --------------------------------------------------
        # Run RAG
        # --------------------------------------------------

        try:
            rag_service = RAGService()

            result = rag_service.ask(
                question=question,
                k=k,
                document_ids=document_ids,
            )

        except Exception as exc:
            return Response(
                {
                    "error": (
                        "Failed to generate an answer."
                    ),
                    "detail": str(exc),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # --------------------------------------------------
        # Save assistant message
        # --------------------------------------------------

        assistant_message = Message.objects.create(
            conversation=conversation,
            role=Message.Role.ASSISTANT,
            content=result["answer"],
            sources=result["sources"],
        )

        # --------------------------------------------------
        # Update conversation timestamp
        # --------------------------------------------------

        conversation.save(
            update_fields=["updated_at"]
        )

        # --------------------------------------------------
        # Return response
        # --------------------------------------------------

        return Response(
            {
                "conversation_id": conversation.id,
                "message_id": assistant_message.id,
                "answer": result["answer"],
                "sources": result["sources"],
            },
            status=status.HTTP_200_OK,
        )


class ConversationDetailView(APIView):

    def get(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(
                id=conversation_id
            )

        except Conversation.DoesNotExist:
            return Response(
                {
                    "error": (
                        "Conversation not found."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ConversationSerializer(
            conversation
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )