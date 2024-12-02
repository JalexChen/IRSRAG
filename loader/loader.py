from langchain.schema import Document
from utils import loader_mapping, splitter_mapping
from database import db
import os

class DocumentLoader:
    def __init__(self):
      self.data_path = os.getenv("DOWNLOAD_DIRECTORY") or "download"
      self.db = db.Database()

    def main(self) -> None:
      self.load_documents()

    def load_documents(self):
      """
      Because we have different types of files, import a mapping for which one to use. Right now, PyPDF is used for PDFs; unstructured
      might be better for this, but this is what we're going with at the moment because it works
      """
      for doc_type, loader_cls in loader_mapping.items():
        path = os.path.join(self.data_path, doc_type)
        self.check_directories(path)

        try:
          loader = loader_cls(path)
          documents = loader.load()
          print(f"Loaded {len(documents)} documents from {path}")
          chunks = self.splitter(documents, doc_type)
          if len(chunks) < 1:
             continue
          self.db.save_to_chroma(chunks)

        except Exception as e:
          print(f"Failed to load documents from {path}: {e}")

    def check_directories(self, path: str) -> None:
      """
      Create directories if it doesn't exist; defaults to "download" unless specified, and makes a subdirectory by filetype
      e.g markdown, html, text, or PDF
      """
      try:
        os.makedirs(path, exist_ok=True)
        print(f"Directory: '{path}' created or exists")
      except Exception as e:
         print(f"Error occurred: {e}")

    def splitter(self, documents: list[Document], doc_type: str) -> list[str]:
      """
      Each type of file will likely have different optimal chunking size, overlap, and lengths. modify splitter_mapping in utils to
      desired preferences based on  your needs
      """
      split = splitter_mapping[doc_type]
      return split.split_documents(documents)

if __name__ == "__main__":
    embedder = DocumentLoader()
    embedder.main()
