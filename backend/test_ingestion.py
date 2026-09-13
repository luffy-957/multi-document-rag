# from pathlib import Path

# from rag.services.ingestion_service import IngestionService


# PDF_PATH = Path(
#     "media/documents/test.pdf"
# )

# DOCUMENT_ID = 1


# def main():
#     service = IngestionService()

#     result = service.ingest_document(
#         file_path=str(PDF_PATH),
#         document_id=DOCUMENT_ID,
#     )

#     print()
#     print("=" * 70)
#     print("INGESTION RESULT")
#     print("=" * 70)

#     print(f"Document ID: {result['document_id']}")
#     print(f"Chunk count: {result['chunk_count']}")

#     print()
#     print("First vector ID:")

#     if result["vector_ids"]:
#         print(result["vector_ids"][0])

#     print("=" * 70)


# if __name__ == "__main__":
#     main()

from pathlib import Path

from rag.services.ingestion_service import IngestionService
from rag.services.vector_store import VectorStore


PDF_PATH = Path(
    "media/documents/test.pdf"
)

DOCUMENT_ID = 1


def main():
    ingestion_service = IngestionService()

    result = ingestion_service.ingest_document(
        file_path=str(PDF_PATH),
        document_id=DOCUMENT_ID,
    )

    print()
    print("=" * 70)
    print("INGESTION RESULT")
    print("=" * 70)

    print(f"Document ID: {result['document_id']}")
    print(f"Chunk count: {result['chunk_count']}")

    print()
    print("=" * 70)
    print("TESTING RETRIEVAL")
    print("=" * 70)

    vector_store = VectorStore()

    query = input(
        "\nAsk a question about the PDF: "
    )

    results = vector_store.similarity_search(
        query,
        k=4,
    )

    print()
    print(f"Retrieved {len(results)} chunks")

    for index, document in enumerate(
        results,
        start=1,
    ):
        print()
        print("-" * 70)
        print(f"RESULT {index}")
        print("-" * 70)

        print(
            f"Source: "
            f"{document.metadata.get('source')}"
        )

        print(
            f"Page: "
            f"{document.metadata.get('page', 0) + 1}"
        )

        print(
            f"Chunk: "
            f"{document.metadata.get('chunk_index')}"
        )

        print()
        print(document.page_content[:1000])


if __name__ == "__main__":
    main()