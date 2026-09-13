from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class PDFProcessor:
    """
    Handles PDF loading and text chunking.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def load_pdf(self, file_path: str):
        """
        Load a PDF and return LangChain Document objects.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {file_path}"
            )

        if path.suffix.lower() != ".pdf":
            raise ValueError(
                "Only PDF files are supported."
            )

        loader = PyMuPDFLoader(str(path))

        return loader.load()

    def split_documents(self, documents):
        """
        Split loaded documents into smaller chunks
        while preserving source metadata.
        """

        chunks = self.text_splitter.split_documents(
            documents
        )

        for index, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = index

        return chunks

    def process(
        self,
        file_path: str,
        document_id: int | None = None,
    ):
        """
        Load a PDF, split it into chunks, and attach
        application-level metadata.
        """

        documents = self.load_pdf(file_path)

        chunks = self.split_documents(documents)

        for chunk in chunks:
            if document_id is not None:
                chunk.metadata["document_id"] = document_id

        return chunks