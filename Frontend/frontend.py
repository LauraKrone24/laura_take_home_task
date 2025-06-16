
import gradio as gr
import ollama
import chromadb
import os
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain import PromptTemplate
from langchain.retrievers import ParentDocumentRetriever
from langchain.docstore.document import Document
from langchain.storage import InMemoryStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain.schema import StrOutputParser
from langchain.prompts.chat import ChatPromptTemplate
from my_helpers import *
import os
import regex as re
print(os.environ['MODELL'])
print(os.environ['EMBEDDING_MODELL'])
print(os.environ['BASE_URL_OLLAMA_CONTAINER'])
LLM_Chain = None
my_retriever = None
def setup_ollama():
    ollama_client = ollama.Client(host =os.environ['BASE_URL_OLLAMA_CONTAINER'] )
    print("Setting up Ollama...")
    ollama_client.pull(os.environ['MODELL'])
    print("Pulled generating model")
    ollama_client.pull(os.environ['EMBEDDING_MODELL'])
    print("Pulled embedding model")
    
    

def create_retriever():
    docs = []
    ids = []
    for file in os.listdir("./text_files"):
        with open("./text_files/"+file, 'r') as open_file:
            text = open_file.read().replace("\n", " ")
            doc = Document(page_content=text, metadata={"source": "local","document_name": file})
            docs.append(doc)
            id= doc.metadata["document_name"]
            ids.append(id)


    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap = 200)
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap = 100)
    embedding_function = OllamaEmbeddings(model=os.environ["EMBEDDING_MODELL"])
    embedding_function.base_url = os.environ['BASE_URL_OLLAMA_CONTAINER']
    vectorstore = Chroma(
            client = chromadb.HttpClient(host="my_chroma_db", port=8000),
            collection_name="take_home_collection",
            embedding_function= embedding_function
        )
    store = InMemoryStore()  # could be changed if out of memory 
    retriever = ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=store,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter,
    )


    retriever.add_documents(docs)

    return retriever

def retrieve_context(dict): 
    print(dict)
    global my_retriever
    documents = my_retriever.invoke(dict["question"])     
    return {"context": format_context(documents), "question": dict["question"], "history_text":dict["history_text"]}

def create_llmchain():

    ollama = Ollama(model=os.environ["MODELL"] )
    ollama.base_url= os.environ['BASE_URL_OLLAMA_CONTAINER']

    prompt_template = ChatPromptTemplate.from_messages([
                HumanMessagePromptTemplate(
                    prompt=PromptTemplate(
                        template=
                        prompt+"###  Answer the question based on the information in the context.\nQuestion: {question}\nContext:\n{context}\nChat history: {history_text}\nAntwort:",
                        input_variables=["question", "context", "history_text"],
                    )
                )])

    llmchain  = (
        {"question": RunnablePassthrough()|format_question, "history_text":RunnablePassthrough()|format_history}
        | RunnableLambda(retrieve_context)
        | prompt_template
        | ollama
        | StrOutputParser()
    )
    return llmchain

def generate_response(message, history):
    global LLM_Chain
    if len(history)>10:
            history = history[:-9]
    history_text = str(history).strip('[]')
    history_text = re.sub(r"<span class=\".{3,6}\">Kontextscore: \d\.\d*<\/span>", "", history_text)
    response = LLM_Chain.invoke({
        "question": message,
        "history_text": history_text,
    })
    return response

def main():
   demo = gr.ChatInterface(
       fn = generate_response,
       type="messages"
   )
   return demo
       
         
if __name__ == "__main__":
    setup_ollama()
    print("Ollama Setup complete!")
    my_retriever = create_retriever()
    print("Retriever Setup Complete")
    LLM_Chain = create_llmchain()
    print("LLMChain Setup Complete")
    print("!!!!    SETUP COMPLETE   !!!!!")
    main().launch(share=False, server_name="0.0.0.0", inbrowser=False, root_path="/")