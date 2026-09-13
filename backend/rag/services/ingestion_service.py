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

        vector_ids = self.vector_store.add_documents(
            chunks
        )

        return {
            "document_id": document_id,
            "chunk_count": len(chunks),
            "vector_ids": vector_ids,
        }