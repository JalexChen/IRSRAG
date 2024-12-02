# IRSRAG
Chatbot leveraging OpenAI embeddings and RAG to provide relevant answers to Tax questions

# Rationale
I wanted to delve a bit deeper into how LLMs work, e.g tokenization, chunking, transformers, but I don't necessarily want to train a specific model since that costs an exorbitant amount of money, and I don't have the data to do it. There are a couple of industries that exist in a space where official documents exist and can be readily accessed without needing any special credentials. Despite the mundane topic, taxes and the IRS provided an outlet for me to simply try out a RAG workflow and allowed me to actually get started on making this happen. It can be applied to many industries that have a corpus of information, e.g healthcare, customer service, education, legal, advertising, and research, but I chose taxes due to a chat I had with someone at FloQast.

The project is technically still a WIP, since I want to add a UI, but in it's current state, you would be able to run this as is by module to parse, download, embed, load, and query the data. The similarity and relevancy score results are then piped into OpenAI in order to provide specific answers to questions due to it's nature in analyzing the entire context of a question.

I've found that the quality of answers is significantly greater than what can be achieved by chunking alone. All in all, where the project is was a great learning experience for me even if it has no commercial benefit. in the future, I'd want to delve a bit deeper into business problems: needs, wants, and goals to actually build something of value and provide an impact.

# Usage
This command crawls, scrapes, maps out different links available on a website:
`python -m firecrawler.crawl -u/--url "url" -a/--action "method" (crawl, scrape, map)`
- crawl will download the contents of a webpage and recursively search for additional pages and save them to the chroma db in a format you specify; markdown is default
- scrape will output the contents of a specific webpage, but does not save the content down; mainly used for discovery
-  map will recursively map available links, such as pdf, markdown, etc, and save it to the specified directory
`python -m loader.loader` will chunk, tokenize, index, and embed the chunks in the vector database
`python query_data.py "query"` will extract relevant information from the documents in the vector database, which then calls the OpenAI LLM to provide you with relevant results

# Issues
I understand that the requirements.txt is... very large. I don't think this should be the case, but I should probably clean this up at some point because honestly there's a lot that shouldn't be in there
