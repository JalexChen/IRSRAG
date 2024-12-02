from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
import os
import shutil

class Database:
  def __init__(self, chroma_path: str | None = None, clear_db: bool | None = None, api_key_env: str = "OPENAI_API_KEY"):
     load_dotenv()
     self.api_key = os.getenv(api_key_env)
     self.chroma_path = os.getenv("CHROMA_PATH") or "chroma"
     self.clear_db = os.getenv("CLEAR_DB") or False
     if self.clear_db == True:
       self._clear_database()

     # Chroma database is currently hosted locally, but can be modified to be hosted elsewhere and executed with a serverless function

  def save_to_chroma(self, chunks: list[Document]) -> None:
    try:
      """
      Currently uses openai embeddings with a default of the ada text dataset; at some point, this can be modified to incorporate
      other embeddings that might make more sense
      """
      db = Chroma(
        persist_directory=self.chroma_path,
        embedding_function=OpenAIEmbeddings(api_key=self.api_key),
      )

      chunks_with_ids = self.calculate_chunk_ids(chunks)
      existing_items = db.get(include=[])
      existing_ids = set(existing_items["ids"])
      print(f"Number of existing documents in DB: {len(existing_ids)}")

      new_chunks = [
        chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids
      ]

      if new_chunks:
        print(f"Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
      else:
        print("No new documents to add")
    except Exception as e:
      print(f"Unable to save to path {self.chroma_path}: {e}")

  def calculate_chunk_ids(self, chunks: list[Document]) -> list[Document]:
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
      # Source parsing to output only the filename itself in response, rather than the full directory where it's located
      source_path = chunk.metadata.get("source")
      source = source_path.split("/")[-1].split(".")[0]
      page = chunk.metadata.get("page")
      current_page_id = f"{source}:{page}"

      if current_page_id == last_page_id:
        current_chunk_index += 1
      else:
        current_chunk_index = 0

      chunk_id = f"{current_page_id}:{current_chunk_index}"
      last_page_id = current_page_id
      chunk.metadata["id"] = chunk_id

    return chunks

  def _clear_database(self) -> None:
    if os.path.exists(self.chroma_path):
      shutil.rmtree(self.chroma_path)

if __name__ == "__main__":
  db = Database()
