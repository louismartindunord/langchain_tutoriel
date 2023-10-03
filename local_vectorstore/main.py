import langchain
import os 
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS 
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
 
from dotenv import load_dotenv
from regex import F
load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def main():
    pdf_path = "./docs/fonctionnement_llm.pdf"
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    text_splitter =  CharacterTextSplitter(
        separator="\n",
        chunk_size= 1000, 
        chunk_overlap=30)
    docs = text_splitter.split_documents(documents=documents)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embedding=embeddings)
    vectorstore.save_local("faiss_index_react")
    new_vectorstore = FAISS.load_local("faiss_index_react", embeddings)
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=new_vectorstore.as_retriever())
    res = qa.run("Explain to me what is llm in 3 sentences")
    print(res)





if __name__ == "__main__":
    main()