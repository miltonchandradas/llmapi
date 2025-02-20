from api_keys import openai_api_key
from flask import Flask, request
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

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

if __name__ == "__main__":
    print("Serving Initializing")
    init()
    print("Serving Started")

    app.run(host="0.0.0.0", port=5000, debug=True)