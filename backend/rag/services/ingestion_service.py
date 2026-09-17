from .pdf_processor import PDFProcessor
from .vector_store import VectorStore


class IngestionService:
    """
    Handles the complete document ingestion pipeline.
    """

    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.vector_store = VectorStore()

    def ingest_document(
        self,
        file_path: str,
        document_id: int,
    ):
        """
        Process a PDF and store its chunks in ChromaDB.
        """

        chunks = self.pdf_processor.process(
            file_path=file_path,
            document_id=document_id,
        )

        if not chunks:
            raise ValueError(
                "No text could be extracted from the PDF."
            )

        # Remove any previously indexed chunks belonging
        # to this document before inserting the new version.
        self.vector_store.delete_document(
            document_id
        )

        vector_ids = self.vector_store.add_documents(
            chunks
        )

        return {
            "document_id": document_id,
            "chunk_count": len(chunks),
            "vector_ids": vector_ids,
        }

    def delete_document(
        self,
        document_id: int,
    ):
        """
        Remove a document's vectors from ChromaDB.
        """

        self.vector_store.delete_document(
            document_id
        )