from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts.chat import ChatPromptTemplate
from dotenv import load_dotenv
import argparse
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
chroma_path = os.getenv("CHROMA_PATH")
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {query}
"""

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("query_text", type=str, help="The query text")
  args = parser.parse_args()
  query_text = args.query_text

  embedding_function = OpenAIEmbeddings(api_key=api_key)

  db = Chroma(persist_directory=chroma_path, embedding_function=embedding_function)
  results = db._similarity_search_with_relevance_scores(query_text, k=3)
  if len(results) == 0 or results[0][1] < 0.7:
    print(f"Unable to find a relevant answer. Using a similarity search...")
    results = db.similarity_search_with_score(query_text, k=5)

  context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
  sources = [doc.metadata.get("id", None) for doc, _score in results]
  specific_answer(context_text, query_text, sources)

def specific_answer(context, query, source) -> str:
  llm = ChatOpenAI(model="gpt-4")
  template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
  prompt = template.format(context=context, query=query)
  response = llm.invoke(prompt)
  formatted_response = f"Response: {response}\n Source: {source}"
  print(formatted_response, "content of response")
  return formatted_response

if __name__ == "__main__":
  main()
