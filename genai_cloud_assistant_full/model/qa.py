import os
from dotenv import load_dotenv  # Add this
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI

# 👇 Load environment variables here too
load_dotenv()

def get_genai_response(prompt: str) -> str:
    try:
        embeddings = OpenAIEmbeddings(openai_api_key="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")
        # vectorstore = FAISS.load_local("vector_db", embeddings)
        vectorstore = FAISS.load_local("model/", embeddings, allow_dangerous_deserialization=True)

        retriever = vectorstore.as_retriever()
        llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-4o-mini")
        qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
        response = qa_chain.run(prompt)
        return response
    except Exception as e:
        return f"Error: {str(e)}"
    
print("Loaded OpenAI Key:", os.getenv("OPENAI_API_KEY"))
