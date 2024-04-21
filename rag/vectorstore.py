from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from utils import load_config

config = load_config()
OPENAI_API_KEY = config["OPENAI"]["API_KEY"]
OPENAI_EMBEDDING_MODEL = config["OPENAI"]["EMBEDDING_MODEL"]

def load_documents():
    urls = [
        "https://lilianweng.github.io/posts/2023-06-23-agent/",
        "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
        "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
    ]

    documents = [WebBaseLoader(url).load() for url in urls]
    documents = [item for sublist in documents for item in sublist]

    return documents

def load_vectorstore():
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250, chunk_overlap=0
    )

    documents = load_documents()
    documents = text_splitter.split_documents(documents)

    vectorstore = Chroma.from_documents(
        documents=documents,
        collection_name="rag-chroma",
        embedding=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model=OPENAI_EMBEDDING_MODEL),
    )

    return vectorstore