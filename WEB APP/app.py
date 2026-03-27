from flask import Flask, render_template, request, redirect, url_for,jsonify
import os
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_classic.chains import ConversationalRetrievalChain
import faiss
import pickle

model = ChatOllama(model = "mistral")

prompt = PromptTemplate.from_template("""Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.
                                      chat_history:{chat_history}
                                      follow up input: {question}
                                      standalone question:""")
parser = StrOutputParser()

from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings


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
db_qa = ConversationalRetrievalChain.from_llm(
    llm=model, 
    retriever=retriever,
    return_source_documents=True
)

# import faiss
# import pickle
# from langchain_community.vectorstores import FAISS
# from langchain_ollama import OllamaEmbeddings

# # 1. Setup embeddings (must match what was used to create the index)
# embeddings = OllamaEmbeddings(model="mistral")

# # 2. Load your raw FAISS index
# index = faiss.read_index("my_python_faiss_index/index.faiss")

# # 3. Load your sentences/documents from the pkl
# with open("my_python_faiss_index/index.pkl", "rb") as f:
#     # Use a single variable to avoid the 'unpack' error
#     data = pickle.load(f) 
    
#     # If your pkl is just a list of sentences, use that. 
#     # If it's a complex dict, you'll need to find the list of texts inside it.
#     texts = data if isinstance(data, list) else data['sentences'] 

# # 4. Rebuild the LangChain-compatible version
# # This step creates the 'docstore' structure LangChain needs
# vector_store = FAISS.from_texts(texts, embeddings)

# # 5. Save it correctly for your Flask app
# vector_store.save_local("my_python_faiss_index_fixed")

# print("Fixed index saved to 'my_python_faiss_index_fixed'")


# py_qa = ConversationalRetrievalChain.from_llm(
#     llm = model,
#     retriever = vector_store.as_retriever(),
#     return_source_documents = True
# )


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

@app.route("/api/query_teacher", methods=["POST"])
def query_teacher():
    data = request.json
    user_query = data.get("query")
    teacher_type = data.get("teacher") # This will be 'db' or 'py'
    if teacher_type == "db":
        chain =db_qa
    elif teacher_type == "py":
        chain = py_qa

    
    # Simple way to handle history for now (or pass it from frontend)
    chat_history = [] 
    
    try:
        # Using the QA chain directly (it handles rephrasing internally)
        result = chain.invoke({"question": user_query, "chat_history": chat_history})
        
        return jsonify({
            "answer": result["answer"],
            "sources": [doc.metadata for doc in result.get("source_documents", [])]
        })
    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=8000)