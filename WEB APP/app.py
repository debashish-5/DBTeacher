from flask import Flask, render_template, request, redirect, url_for
import os
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_classic.chains import ConversationalRetrievalChain
import faiss
model = ChatOllama(model = "mistral")

prompt = PromptTemplate.from_template("""Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.
                                      chat_history:{chat_history}
                                      follow up input: {question}
                                      standalone question:""")
parser = StrOutputParser()

from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain.chains import ConversationalRetrievalChain

# 1. Initialize your embedding model
embeddings = OllamaEmbeddings(model="mistral")

# 2. Load the index from your local folder
# Make sure "my_faiss_index" contains both index.faiss and index.pkl
vector_store = FAISS.load_local(
    "my_faiss_index", 
    embeddings, 
    allow_dangerous_deserialization=True
)

# 3. Create the retriever from the loaded store
retriever = vector_store.as_retriever()

# 4. Integrate into your existing chain
qa = ConversationalRetrievalChain.from_llm(
    llm=model, 
    retriever=retriever,
    return_source_documents=True
)



app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/py-teacher")
def pyteacher():
    return render_template("py_teacher.html")

@app.route("/db-teacher")
def dbteacher():
    return render_template("db_teacher.html")

@app.route("/all-rounder")
def allrounder():
    return render_template("all_rounder.html")

@app.route("/ask",methods=["POST"])
def ask():
    question = request.form["question"]
    chat_history = []
    # Rephrase the question to be standalone
    standalone_question = parser.parse(model(prompt.format(chat_history=chat_history, question=question)))
    # Get the answer from the QA chain
    result = qa({"question":standalone_question,"chat_history":chat_history})
    answer = result["answer"]
    # Update chat history
    chat_history.append((question, answer))
    return render_template("db_teacher.html",question=question,result=result)

# app.route()
if __name__ == "__main__":
    app.run(debug=True, port=8000)