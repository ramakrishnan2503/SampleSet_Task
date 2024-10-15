import streamlit as st
from chatbot import get_pdf_text, get_vector_store, user_input

def main():
    st.set_page_config("Chat With Documents", layout="wide")
    st.title("Chat with PDF using Gemini Pro")

    with st.sidebar:
        st.header("Upload & Process")
        pdf_docs = st.file_uploader("Upload your PDF Files", accept_multiple_files=True)
        
        if st.button("Submit & Process"):
            if pdf_docs:
                with st.spinner("Processing your PDFs..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_vector_store(raw_text)
                    st.success("PDFs processed successfully!")
            else:
                st.warning("Please upload at least one PDF file.")

    st.header("Ask Questions")
    user_question = st.text_input("Ask a question related to the uploaded document:")
    
    if user_question:
        if st.button("Submit Question"):
            with st.spinner("Fetching your answer..."):
                response, matched_docs = user_input(user_question)
                
                st.write("**Response:**", response)
                
                st.write("**Retrieved Document Segments:**")
                for idx, doc in enumerate(matched_docs):
                    st.write(f"**Segment {idx + 1}:** {doc}")

if __name__ == "__main__":
    main()
