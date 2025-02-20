from api_keys import openai_api_key
from flask import Flask, request
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from pydantic import BaseModel, Field

import os
import json

# Creates Flask serving engine
app = Flask(__name__)
appHasRunBefore = False
os.environ["OPENAI_API_KEY"] = openai_api_key

@app.before_request
def init():
    # Set up langchain
    global appHasRunBefore
    global chat_llm

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

if __name__ == "__main__":
    print("Serving Initializing")
    init()
    print("Serving Started")

    app.run(host="0.0.0.0", port=5000, debug=True)