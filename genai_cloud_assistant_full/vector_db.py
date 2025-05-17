# import os
# from dotenv import load_dotenv
# from langchain.vectorstores import FAISS
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.document_loaders import TextLoader
# from langchain.text_splitter import CharacterTextSplitter

# load_dotenv()

# def build_vector_store():
#     # Load some documents - update path to your actual docs
#     loader = TextLoader("docs/sample.txt")
#     documents = loader.load()

#     # Split into chunks
#     splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
#     docs = splitter.split_documents(documents)

#     # Create embeddings
#     embeddings = OpenAIEmbeddings(openai_api_key="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")

#     # Create vector store and save locally
#     vectorstore = FAISS.from_documents(docs, embeddings)
#     vectorstore.save_local("vector_db")

#     print("Vector DB built and saved in 'vector_db' directory.")

# if __name__ == "__main__":
#     build_vector_store()
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY="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"
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not found in .env file.")

def build_vector_store():
    loader = TextLoader("docs/sample.txt")
    documents = loader.load()

    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("model")

    print("✅ Vector DB built and saved in 'model' directory.")

if __name__ == "__main__":
    build_vector_store()
