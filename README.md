# Chat with PDF using Gemini Pro

This project provides a simple interface to interact with PDFs using a Question-Answering (QA) chatbot. The chatbot allows users to upload PDFs, process them, and ask questions about their content. It uses **Google Generative AI (Gemini Pro)** for embedding and conversation generation, **Langchain** for question answering, and **FAISS** for vector storage.

## Features

- **PDF Upload**: Users can upload one or more PDFs.
- **PDF Processing**: Extracts text from PDFs and splits it into manageable chunks.
- **Embeddings**: Uses Google Generative AI embeddings to represent the PDF content in a semantic vector space.
- **Vector Search**: FAISS is used to search for relevant document chunks based on the user's query.
- **Question Answering**: Provides detailed answers based on the context of the retrieved PDF document chunks. If the chatbot cannot confidently answer a question, it will respond with: *"The information is not available in the document."*

## Project Structure

- `chatbot.py`: Contains all the core logic for processing PDFs, embedding text, and answering questions.
- `app.py`: The frontend of the application using **Streamlit**. It allows users to upload PDFs, ask questions, and receive answers.


## How It Works

### 1. PDF Text Extraction:
- Extracts text from uploaded PDF files using **PyPDF2**.
- Uses the **RecursiveCharacterTextSplitter** from **Langchain** to split large documents into smaller chunks for efficient retrieval.

### 2. Embeddings and Vector Store:
- Uses **GoogleGenerativeAIEmbeddings** to embed the chunks of text.
- Stores the embedded chunks in **FAISS**, a vector search engine, for fast retrieval during question answering.

### 3. Question Answering:
- When a user asks a question, the system performs a similarity search on the vector store.
- The retrieved chunks are passed through a QA chain, and the **Google Generative AI (gemini-pro)** model generates a response based on the context of the documents.



## Installation

Follow these steps to set up the project:
  
  ### 1. Clone the Repository
  
  ```bash
  git clone https://github.com/ramakrishnan2503/SampleSet_Task.git
  cd SampleSet_Task
  ```

  ### 2. Install Dependencies
  
  You can install the necessary dependencies using pip:
  
  ```bash
  pip install -r requirements.txt
  ```
  
  ### 3. Set Up Environment Variables
  
  Create a .env file in the root directory of your project and add your Google API key:
  
  ```bash
  GOOGLE_API_KEY=your-google-api-key
  ```
  
  ### 4. Run the Application
  
  You can start the Streamlit app by running:
  
  ```bash
  streamlit run app.py
  ```
