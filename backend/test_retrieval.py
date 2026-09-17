from rag.services.vector_store import VectorStore


def main():
    vector_store = VectorStore()

    query = input(
        "Ask a question about your documents: "
    )

    results = vector_store.similarity_search(
        query=query,
        k=4,
    )

    print()
    print("=" * 70)
    print("RETRIEVAL RESULTS")
    print("=" * 70)

    print(f"Retrieved {len(results)} chunks.")

    for index, document in enumerate(
        results,
        start=1,
    ):
        print()
        print("-" * 70)
        print(f"RESULT {index}")
        print("-" * 70)

        print(
            "Document ID:",
            document.metadata.get("document_id"),
        )

        print(
            "Source:",
            document.metadata.get("source"),
        )

        print(
            "Page:",
            document.metadata.get("page", 0) + 1,
        )

        print(
            "Chunk:",
            document.metadata.get("chunk_index"),
        )

        print()
        print(document.page_content[:1000])


if __name__ == "__main__":
    main()