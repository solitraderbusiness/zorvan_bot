"""PDF text extraction service."""
from PyPDF2 import PdfReader


class PDFService:
    """Service for extracting text from PDF files."""

    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """
        Extract text from a PDF file.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Extracted text
        """
        print(f"Extracting text from PDF: {pdf_path}")

        reader = PdfReader(pdf_path)
        text = ""

        for page_num, page in enumerate(reader.pages, 1):
            page_text = page.extract_text()
            text += f"\n--- Page {page_num} ---\n{page_text}"

        print(f"Extracted {len(text)} characters from PDF")
        return text


# Singleton instance
pdf_service = PDFService()
