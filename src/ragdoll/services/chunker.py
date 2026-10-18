## -- Text chunking module

from langchain_text_splitters import RecursiveCharacterTextSplitter

from ragdoll.core.config import settings

# SPLIT TEXT IN OVERLAPPING CHUNKS
def chunk_text(text: str, size: int = 800, overlap: int = 100) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = settings.chunk_size,
        # overlap allows for better recall,
        # as it links together chunks of the text
        chunk_overlap = settings.chunk_overlap
    )
    chunks = splitter.split_text(text)
    return chunks
