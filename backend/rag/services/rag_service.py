from .llm_service import LLMService
from .vector_store import VectorStore
from pathlib import Path

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
        history: str = "",
    ):
        """
        Build the prompt given to the LLM.
        """
        return f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the
information provided in the document context.

Rules:

1. Do not use outside knowledge.
2. Do not invent facts.
3. If the answer cannot be found in the
   provided documents, clearly say that the
   information is not available in the documents.
4. Use conversation history only to understand
   references and context.
5. The document context is the authoritative
   source for factual answers.
6. Give a concise and useful answer.
7. When appropriate, mention the relevant
   source and page.

CONVERSATION HISTORY
====================
{history}

DOCUMENT CONTEXT
================
{context}

CURRENT QUESTION
================
{question}

ANSWER
======
"""
#         return f"""
# You are a document question-answering assistant.

# Answer the user's question using ONLY the
# information provided in the context below.

# Rules:

# 1. Do not use outside knowledge.
# 2. Do not invent facts.
# 3. If the answer cannot be found in the context,
#    clearly say that the information is not available
#    in the provided documents.
# 4. Give a concise and useful answer.
# 5. When appropriate, mention which source or page
#    supports the answer.

# CONTEXT
# =======
# {context}

# QUESTION
# ========
# {question}

# ANSWER
# ======
# """

    def ask(
        self,
        question: str,
        k: int = 4,
        document_ids: list[int] | None = None,
        history: list[dict] | None = None,
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

        history_text = self.build_history(
            history or []
        )   

        prompt = self.build_prompt(
            question=question,
            context=context,
            history=history_text,
        )

        answer = self.llm_service.generate(
            prompt
        )

        # sources = []

        # for document in documents:
        #     sources.append(
        #         {
        #             "source": document.metadata.get(
        #                 "source"
        #             ),
        #             "page": (
        #                 document.metadata.get(
        #                     "page",
        #                     0,
        #                 )
        #                 + 1
        #             ),
        #             "chunk_index": document.metadata.get(
        #                 "chunk_index"
        #             ),
        #             "document_id": document.metadata.get(
        #                 "document_id"
        #             ),
        #         }
        #     )

        sources = []

        seen_sources = set()

        for document in documents:
            document_id = document.metadata.get(
                "document_id"
            )

            source = document.metadata.get(
                "source",
                "Unknown source",
            )

            filename = Path(source).name

            page = (
                document.metadata.get("page", 0)
                + 1
            )

            chunk_index = document.metadata.get(
                "chunk_index"
            )

            source_key = (
                document_id,
                filename,
                page,
            )

            if source_key in seen_sources:
                continue
            
            seen_sources.add(source_key)

            sources.append(
                {
                    "document_id": document_id,
                    "document": filename,
                    "page": page,
                    "chunk_index": chunk_index,
                }
            )

        return {
            "answer": answer,
            "sources": sources,
        }

    def build_history(self, messages):
        if not messages:
            return ""

        history_parts = []

        for message in messages:
            role = message.get("role", "user").upper()
            content = message.get("content", "")

            history_parts.append(
                f"{role}: {content}"
            )

        return "\n".join(history_parts)