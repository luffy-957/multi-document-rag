from rest_framework import serializers

from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            "id",
            "title",
            "file",
            "status",
            "uploaded_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "status",
            "uploaded_at",
            "updated_at",
        )

    def validate_file(self, value):
        if not value.name.lower().endswith(".pdf"):
            raise serializers.ValidationError(
                "Only PDF files are allowed."
            )

        if value.size > 20 * 1024 * 1024:
            raise serializers.ValidationError(
                "PDF file size must not exceed 20 MB."
            )

        return value