from .llm_service import LLMService
from .vector_store import VectorStore


class RAGService:
    """
    Handles retrieval-augmented generation.
    """

    def __init__(self):
        self.vector_store = VectorStore()
        self.llm_service = LLMService()

    def retrieve(
        self,
        query: str,
        k: int = 4,
        document_ids: list[int] | None = None,
    ):
        """
        Retrieve relevant chunks from ChromaDB.
        """

        return self.vector_store.similarity_search(
            query=query,
            k=k,
            document_ids=document_ids,
        )

    def build_context(self, documents):
        """
        Convert retrieved documents into a context string.
        """

        context_parts = []

        for index, document in enumerate(
            documents,
            start=1,
        ):
            source = document.metadata.get(
                "source",
                "Unknown source",
            )

            page = document.metadata.get(
                "page",
                0,
            )

            page_number = page + 1

            context_parts.append(
                f"""
SOURCE {index}
File: {source}
Page: {page_number}

Content:
{document.page_content}
"""
            )

        return "\n".join(context_parts)

    def build_prompt(
        self,
        question: str,
        context: str,
    ):
        """
        Build the prompt given to the LLM.
        """

        return f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the
information provided in the context below.

Rules:

1. Do not use outside knowledge.
2. Do not invent facts.
3. If the answer cannot be found in the context,
   clearly say that the information is not available
   in the provided documents.
4. Give a concise and useful answer.
5. When appropriate, mention which source or page
   supports the answer.

CONTEXT
=======
{context}

QUESTION
========
{question}

ANSWER
======
"""

    def ask(
        self,
        question: str,
        k: int = 4,
        document_ids: list[int] | None = None,
    ):
        """
        Retrieve relevant documents and generate an answer.
        """

        documents = self.retrieve(
            query=question,
            k=k,
            document_ids=document_ids,
        )

        if not documents:
            return {
                "answer": (
                    "I could not find relevant information "
                    "in the provided documents."
                ),
                "sources": [],
            }

        context = self.build_context(
            documents
        )

        prompt = self.build_prompt(
            question=question,
            context=context,
        )

        answer = self.llm_service.generate(
            prompt
        )

        sources = []

        for document in documents:
            sources.append(
                {
                    "source": document.metadata.get(
                        "source"
                    ),
                    "page": (
                        document.metadata.get(
                            "page",
                            0,
                        )
                        + 1
                    ),
                    "chunk_index": document.metadata.get(
                        "chunk_index"
                    ),
                    "document_id": document.metadata.get(
                        "document_id"
                    ),
                }
            )

        return {
            "answer": answer,
            "sources": sources,
        }