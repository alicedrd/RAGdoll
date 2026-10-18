# -- parsing module
from pathlib import Path
import pypdf
import io
import mimetypes

from ragdoll.core.exceptions import UnsupportedDocTypeError

# pdf parser
def _parse_pdf(src: io.BytesIO) -> str:
    reader = pypdf.PdfReader(src)
    text_per_page: list[str] = []
    for page in reader.pages:
        page_content = page.extract_text()
        if page_content:
            text_per_page.append(page_content)
    text = "\n\n".join(text_per_page) # add page separator
    
    return text

_PARSERS = {
    "application/pdf": _parse_pdf
}

# exposed set containing all mime types i assigned a parsing function to
SUPPORTED_MIME_TYPES = _PARSERS.keys()

# exposed function that can parse any supported document
def parse_doc(src: io.BytesIO, orig_filename: str, mime: str) -> str:
    parser = _PARSERS.get(mime)
    if not parser:
        raise UnsupportedDocTypeError(orig_filename, mime)
    return parser(src)