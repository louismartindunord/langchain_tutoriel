from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain import VectorDBQA
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI


import os
import pinecone

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY =  os.environ.get("PINECONE_API_KEY")


def main():
    pinecone.init(  
        api_key = PINECONE_API_KEY,
        environment = "us-west4-gcp-free"
    )
    index_name = "langchain-demo"
    
    if index_name not in pinecone.list_indexes():
    # we create a new index
        pinecone.create_index(
          name=index_name,
          metric='euclidean',
          dimension=1536  
        )
        
    #try : 
       #print("test l'existence de donnée")
        docsearch = Pinecone.from_existing_index(index_name, OpenAIEmbeddings())
       
        #docs = docsearch.similarity_search(query)
        #print(docs[0].page_content)
    #except: 
    loader =  TextLoader("./docs/fonctionnement_llm.txt")
    document = loader.load()
    text_splitter = CharacterTextSplitter(
                                  chunk_size=1000,
                                  chunk_overlap=0
                                 )
    texts = text_splitter.split_documents(document)
    embeddings = OpenAIEmbeddings()
    docsearch = Pinecone.from_documents(texts, embeddings, index_name="langchain-demo")
    
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(),
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        return_source_documents=True
        )


    query = 'what is a llm give me a 50 words answear for a beginner'
    result = qa({"query": query})
    print(result)
        
        


if __name__ == '__main__':
    main()
