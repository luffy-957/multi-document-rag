from rag.services.rag_service import RAGService


def main():
    rag_service = RAGService()

    print()
    print("=" * 70)
    print("MULTI-DOCUMENT RAG")
    print("=" * 70)

    question = input(
        "\nAsk a question about your documents: "
    )

    result = rag_service.ask(
        question=question,
        k=4,
    )

    print()
    print("=" * 70)
    print("ANSWER")
    print("=" * 70)

    print(result["answer"])

    print()
    print("=" * 70)
    print("SOURCES")
    print("=" * 70)

    for index, source in enumerate(
        result["sources"],
        start=1,
    ):
        print(
            f"{index}. "
            f"Document ID: {source['document_id']} | "
            f"Page: {source['page']} | "
            f"Chunk: {source['chunk_index']}"
        )

        print(
            f"   Source: {source['source']}"
        )


if __name__ == "__main__":
    main()