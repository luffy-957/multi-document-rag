from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingService:
    """
    Creates text embeddings using a local HuggingFace model.
    """

    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.MODEL_NAME,
            model_kwargs={
                "device": "cpu",
            },
            encode_kwargs={
                "normalize_embeddings": True,
            },
        )

    def embed_query(self, text: str):
        """
        Convert a single query into an embedding vector.
        """

        return self.embeddings.embed_query(text)

    def embed_documents(self, texts: list[str]):
        """
        Convert multiple text chunks into embedding vectors.
        """

        return self.embeddings.embed_documents(texts)