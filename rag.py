from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from config import google_api_key, groq_api_key

loader = TextLoader("hospital.txt")
docs = loader.load()



gemini_llm = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash',
    google_api_key=google_api_key
)

groq_llm = ChatGroq(
    model = 'llama-3.1-8b-instant',
    groq_api_key=groq_api_key
)

def llm_invoke(prompt):
    try:
        response = gemini_llm.invoke(prompt)
        return response.content

    except Exception as gemini_error:
        print(f"Gemini Error: {gemini_error}")

        try:
            response = groq_llm.invoke(prompt)
            return response.content

        except Exception as groq_error:
            print(f"Groq Error: {groq_error}")
            return "Both Gemini and Groq are currently unavailable."

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100, # Each chunk can contain 100 characters
    chunk_overlap=20 # the next chunl repeats the last 20 characters from previous chunk
)

chunks = splitter.split_documents(docs)

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_db = FAISS.from_documents(
    chunks,
    embedding_model
)

retriever = vector_db.as_retriever(
    search_kwargs={"k": 2} # Return top 2 matching chunks
)

def chat(question):

    retrieved_docs = retriever.invoke(question)

    context = "\n".join(
        [doc.page_content for doc in retrieved_docs]
    )

    prompt = f"""
    You are a helpful hospital assistant.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    response = llm_invoke(prompt)

    return response