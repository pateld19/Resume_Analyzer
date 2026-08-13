import io

from docx import Document
from pypdf import PdfReader


class UnsupportedFileTypeError(ValueError):
    pass


class EmptyTextError(ValueError):
    pass


def _extract_pdf_text(content: bytes) -> str:
    reader = PdfReader(io.BytesIO(content))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages).strip()


def _extract_docx_text(content: bytes) -> str:
    document = Document(io.BytesIO(content))
    paragraphs = [p.text for p in document.paragraphs]
    return "\n".join(paragraphs).strip()


def extract_text(filename: str, content: bytes) -> str:
    lower_name = filename.lower()

    if lower_name.endswith(".pdf"):
        text = _extract_pdf_text(content)
    elif lower_name.endswith(".docx"):
        text = _extract_docx_text(content)
    else:
        raise UnsupportedFileTypeError(
            f"Unsupported file type for '{filename}'. Only .pdf and .docx are supported."
        )

    if not text:
        raise EmptyTextError(
            "No extractable text was found in the resume. "
            "If this is a scanned or image-only PDF, it isn't supported yet."
        )

    return text
