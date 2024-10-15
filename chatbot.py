from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os
import io
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Pinecone
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate 

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def get_pdf_text(pdf_docs):
    text = ""
    
    for pdf in pdf_docs:
        pdf_reader = PdfReader(io.BytesIO(pdf.read()))
        for page in pdf_reader.pages:
            text += page.extract_text()
    
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=500)
    
    return text_splitter.split_text(text)


def get_vector_store(text):
    text_chunks = get_text_chunks(text)
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embeddings)
    vector_store.save_local("faiss_index")
    
    return text_chunks


def get_conversational_chain():
    
    prompt_template = """
    You are a QA bot that answers questions based solely on the provided document. If you are confident in your answer based on the 
    context retrieved from the document, provide a detailed response. If the context does not provide enough information or you are 
    unsure, respond with, 'The information is not available in the document.'
    Context :\n {context}\n
    Question :\n {question}\n
    
    Answer :
    """
    
    model = ChatGoogleGenerativeAI(model='gemini-pro', temperature=0.4)
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)

def user_input(user_question):
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
    
    docs = vector_store.similarity_search(user_question,k=7)
    
    matched_docs = [doc.page_content for doc in docs]
    
    chain = get_conversational_chain()
    
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    
    return response['output_text'], matched_docs
