from api_keys import openai_api_key
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from pydantic import BaseModel, Field

import os
import json

# Creates Flask serving engine
app = Flask(__name__)
CORS(app)
appHasRunBefore = False
os.environ["OPENAI_API_KEY"] = openai_api_key

# Set upload folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
chat_llm = None
db = None

@app.before_request
def init():
    # Set up langchain
    global appHasRunBefore
    global chat_llm
    global db

    if not appHasRunBefore:
        chat_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)  
        
        appHasRunBefore = True
        return None

@app.route("/v1/greeting", methods=["GET"])
def greeting():
    return "Hello...  Welcome to the world of Python..."


@app.route("/v1/joke", methods=["POST"])
def get_joke():
    global chat_llm
    
    query = dict(request.json)
    topic = query["topic"]
    
    prompt_template = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
    output_parser = StrOutputParser()
    
    chain = prompt_template | chat_llm | output_parser
    joke_response = chain.invoke({"topic": topic})
    
    return joke_response


@app.route("/v1/products", methods=["POST"])
def get_products():
    global chat_llm
    
    query = dict(request.json)
    category = query["category"]
    count = query["count"]
    
    class Product(BaseModel):
        name: str = Field(description="Name of product")
        description: str = Field(description="Description of product")   
        price: float = Field(description="Price of the product")
        rating: int = Field(description="Rating of the product from 1 to 5")
        unitsInStock: int = Field(description="Number of units that are in stock")
        
    class Inventory(BaseModel):
        products: list[Product] = Field(description="This is the list of products")

    output_parser = JsonOutputParser(pydantic_object=Inventory)
    
    prompt_template = ChatPromptTemplate(
        messages = [
            ("system", "You are a helpful AI assistant.  \nFormatting Instructions: {format_instructions}"),
            ("human", "Can you create {count} fictitious products for the following category: {category}")
    ])
                                     
    chain = prompt_template | chat_llm | output_parser
    products_response = chain.invoke({
        "category": category,
        "count": count,
        "format_instructions": output_parser.get_format_instructions()
        })
    
    return products_response


@app.route("/v1/uploadPDF", methods=["POST"])
async def upload_pdf():
    global db
    
    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    embeddings_model = OpenAIEmbeddings()
    
    # Create a FAISS vector store from the documents
    db = FAISS.from_documents(documents, embeddings_model)
    
    return jsonify({"message": "File uploaded successfully", "filename": file.filename}), 200


@app.route("/v1/queryPDF", methods=["POST"])
def query_pdf():
    global db
    
    query = dict(request.json)
    question = query["question"]
    
    output_parser = StrOutputParser()
    docs = db.similarity_search(question, k=8)

    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"Context:\n{context}\n\nQuestion: {question}"

    chain = chat_llm | output_parser
    answer = chain.invoke(prompt)
    
    return jsonify({"question": question, "answer": answer}), 200
    
     
if __name__ == "__main__":
    print("Serving Initializing")
    init()
    print("Serving Started")

    app.run(host="0.0.0.0", port=5000, debug=True)