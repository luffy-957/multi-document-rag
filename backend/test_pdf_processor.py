from pathlib import Path

from rag.services.pdf_processor import PDFProcessor


PDF_PATH = Path(
    "media/documents/test.pdf"
)


def main():
    processor = PDFProcessor()

    chunks = processor.process(
        str(PDF_PATH)
    )

    print()
    print("=" * 70)
    print("PDF PROCESSING RESULT")
    print("=" * 70)

    print(f"Number of chunks: {len(chunks)}")

    print()
    print("First chunk:")
    print("-" * 70)

    if chunks:
        print(chunks[0].page_content[:2000])

        print()
        print("Metadata:")
        print(chunks[0].metadata)

    print("=" * 70)


if __name__ == "__main__":
    main()