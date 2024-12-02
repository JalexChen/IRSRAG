from idna import check_nfc
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader, DirectoryLoader

loader_mapping = {
  "pdf": PyPDFDirectoryLoader,
  "markdown": DirectoryLoader,
  "text": DirectoryLoader,
  "html": DirectoryLoader
}

file_extensions = {
  "pdf": ".pdf",
  "markdown": ".md",
  "text": ".txt",
  "html": ".html"
}

splitter_mapping = {
  "text": RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    length_function=len,
    add_start_index=True
  ),
  "markdown": RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    length_function=len,
    add_start_index=True
  ),
  "html": RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    length_function=len,
    add_start_index=True
  ),
  "pdf": RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=80,
    length_function=len,
    is_separator_regex=False,
  )
}


