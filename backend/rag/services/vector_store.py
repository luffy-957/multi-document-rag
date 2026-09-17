from pathlib import Path

from langchain_chroma import Chroma

from .embedding_service import EmbeddingService


class VectorStore:
    """
    Handles persistent ChromaDB storage and retrieval.
    """

    COLLECTION_NAME = "documents"

    def __init__(self):
        project_root = Path(__file__).resolve().parents[3]

        self.persist_directory = (
            project_root / "chroma_db"
        )

        self.embedding_service = EmbeddingService()

        self.vector_store = Chroma(
            collection_name=self.COLLECTION_NAME,
            embedding_function=self.embedding_service.embeddings,
            persist_directory=str(self.persist_directory),
        )

    def add_documents(self, documents):
        """
        Add documents to ChromaDB using deterministic IDs.
        """

        if not documents:
            return []

        ids = []

        for document in documents:
            document_id = document.metadata.get(
                "document_id"
            )

            chunk_index = document.metadata.get(
                "chunk_index"
            )

            if document_id is None:
                raise ValueError(
                    "Every document must have a document_id."
                )

            if chunk_index is None:
                raise ValueError(
                    "Every document must have a chunk_index."
                )

            chunk_id = (
                f"document-{document_id}"
                f"-chunk-{chunk_index}"
            )

            ids.append(chunk_id)

        return self.vector_store.add_documents(
            documents=documents,
            ids=ids,
        )

    def delete_document(self, document_id: int):
        """
        Delete every vector belonging to a Django document.
        """

        self.vector_store.delete(
            where={
                "document_id": document_id
            }
        )

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        document_ids: list[int] | None = None,
    ):
        """
        Return the most relevant chunks.

        If document_ids is provided, retrieval is restricted
        to those documents.
        """

        if document_ids:
            if len(document_ids) == 1:
                filter_condition = {
                    "document_id": document_ids[0]
                }
            else:
                filter_condition = {
                    "$or": [
                        {
                            "document_id": document_id
                        }
                        for document_id in document_ids
                    ]
                }

            return self.vector_store.similarity_search(
                query,
                k=k,
                filter=filter_condition,
            )

        return self.vector_store.similarity_search(
            query,
            k=k,
        )