import os

from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openrouter import ChatOpenRouter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_tavily import TavilySearch


# ---------------------------------------------------------
# Environment
# ---------------------------------------------------------

load_dotenv()

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set.")

if not TAVILY_API_KEY:
    raise RuntimeError("TAVILY_API_KEY is not set.")


# ---------------------------------------------------------
# 1. OpenRouter reasoning model
# ---------------------------------------------------------

model = ChatOpenRouter(
    model="dots-studio/dots-3-note-preview:free",
    temperature=0.1,
    max_tokens=3000,
    max_retries=2,
)


# ---------------------------------------------------------
# 2. BGE-M3 embeddings
# ---------------------------------------------------------


class OpenRouterEmbeddings(OpenAIEmbeddings):
    def embed_documents(self, texts, chunk_size=None, **kwargs):
        embeddings = []
        for text in texts:
            response = self.client.create(model=self.model, input=text)
            embeddings.append(response.data[0].embedding)
        return embeddings

    def embed_query(self, text, **kwargs):
        response = self.client.create(model=self.model, input=text)
        return response.data[0].embedding


embeddings = OpenRouterEmbeddings(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,  # type: ignore
    model="baai/bge-m3",
)


# ---------------------------------------------------------
# 3. Chroma vector database
# ---------------------------------------------------------

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "chroma_db"

vectorstore = Chroma(
    collection_name="research_docs",
    persist_directory=str(DB_DIR),
    embedding_function=embeddings,
)


# ---------------------------------------------------------
# 4. Retriever
# ---------------------------------------------------------

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})


# ---------------------------------------------------------
# 5. RAG tool
# ---------------------------------------------------------


@tool
def retrieve_documents(query: str) -> str:
    """
    Search the internal research knowledge base.

    Use this tool when the question may be answered using
    information contained in the internal documents.
    """

    documents = retriever.invoke(query)

    if not documents:
        return "No relevant internal documents were found."

    results = []

    for i, document in enumerate(
        documents,
        start=1,
    ):
        source = document.metadata.get(
            "source",
            "unknown",
        )

        results.append(
            f"""
SOURCE TYPE: INTERNAL KNOWLEDGE BASE
DOCUMENT: {i}
SOURCE: {source}

CONTENT:
{document.page_content}
"""
        )

    return "\n".join(results)


# ---------------------------------------------------------
# 6. Web search
# ---------------------------------------------------------

web_search = TavilySearch(
    max_results=5,
)


@tool
def search_web(query: str) -> str:
    """
    Search the public web.

    Use this tool for current, recent, external, or
    time-sensitive information that may not exist in
    the internal knowledge base.
    """

    result = web_search.invoke({"query": query})

    return str(result)


# ---------------------------------------------------------
# 7. Agent system prompt
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are a research agent.

Your job is to answer questions accurately using
evidence from the available information sources.

You have two tools.

1. retrieve_documents

This searches the internal knowledge base.

Use it when:
- The question concerns internal documentation.
- The answer may exist in the provided documents.
- The user asks about the internal research-agent system.
- The question concerns concepts contained in the knowledge base.

2. search_web

This searches the public web.

Use it when:
- The user asks for current information.
- The information may have changed recently.
- The question concerns current software releases.
- The internal knowledge base does not contain enough information.
- The user explicitly asks for web research.

Tool selection:

Do not automatically call both tools.

Choose the smallest set of tools needed to answer
the question reliably.

If the question requires both internal and external
information, use both tools.

Evidence rules:

- Do not invent facts.
- Do not pretend that retrieved information exists
  when retrieval returned nothing.
- Distinguish internal information from web information.
- If sources disagree, explicitly state the disagreement.
- Prefer authoritative sources when using web search.
- Base factual claims on retrieved evidence whenever
  possible.
- If there is insufficient evidence, say so.

Answer format:

1. Give the answer first.
2. Explain the important reasoning or evidence.
3. Clearly distinguish internal knowledge from external
   information when both are used.

You are a research agent, not merely a chatbot.
Tool selection and evidence quality are important.
"""


# ---------------------------------------------------------
# 8. Create agent
# ---------------------------------------------------------

agent = create_agent(
    model=model,
    tools=[
        retrieve_documents,
        search_web,
    ],
    system_prompt=SYSTEM_PROMPT,
)


# ---------------------------------------------------------
# 9. Run agent
# ---------------------------------------------------------


def main():

    print("=" * 70)
    print("RESEARCH AGENT")
    print("=" * 70)

    print("\nAvailable tools:")

    print("  - retrieve_documents")

    print("  - search_web")

    while True:
        print("\n" + "-" * 70)

        question = input("Research question: ").strip()

        if not question:
            continue

        if question.lower() in {
            "exit",
            "quit",
        }:
            print("\nExiting.")
            break

        print("\nAgent is researching...\n")

        try:
            result = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": question,
                        }
                    ]
                }
            )

            print("=" * 70)

            print("ANSWER")

            print("=" * 70)

            print(result["messages"][-1].content)

        except Exception as e:
            print("\nAgent error:")

            print(repr(e))


if __name__ == "__main__":
    main()
