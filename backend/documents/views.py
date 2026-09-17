from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from rag.services.ingestion_service import IngestionService

from .models import Document
from .serializers import DocumentSerializer


class DocumentUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = DocumentSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        document = serializer.save()

        try:
            # Tell the database that RAG processing has started.
            document.status = Document.Status.PROCESSING
            document.save(
                update_fields=["status", "updated_at"]
            )

            # Run the RAG ingestion pipeline.
            ingestion_service = IngestionService()

            result = ingestion_service.ingest_document(
                file_path=document.file.path,
                document_id=document.id,
            )

            # Processing succeeded.
            document.status = Document.Status.PROCESSED
            document.save(
                update_fields=["status", "updated_at"]
            )

            return Response(
                {
                    "document": DocumentSerializer(
                        document
                    ).data,
                    "ingestion": {
                        "chunk_count": result[
                            "chunk_count"
                        ],
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as exc:
            # Keep the document record so that we can inspect
            # and eventually retry failed processing.
            document.status = Document.Status.FAILED
            document.save(
                update_fields=["status", "updated_at"]
            )

            return Response(
                {
                    "error": "Document processing failed.",
                    "detail": str(exc),
                    "document": DocumentSerializer(
                        document
                    ).data,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )