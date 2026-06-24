from fastapi import FastAPI
from pydantic import BaseModel
from rag import retriever, llm


app = FastAPI()

class Question(BaseModel):
    query: str

@app.post('/chat')

def chat(question: Question):
  retrieved_docs = retriever.invoke(question.query)

  context = "\n".join(
    [doc.page_content for doc in retrieved_docs]
  )

  prompt = f"""
  You are a helpful hospital assistant.
  Context:
  {context}
  Question:
  {question.query}
  Answer:
  """

  response = llm.invoke(prompt)

  return{
      'question': question.query,
      'answer': response.content
  }

