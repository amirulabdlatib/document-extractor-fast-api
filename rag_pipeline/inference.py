from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

TEMPERATURE = 0.0
MODEL = 'deepseek-r1:8b'
BASE_URL = 'http://localhost:11434/'

llm = ChatOllama(temperature=TEMPERATURE,model=MODEL,base_url=BASE_URL)
results = {}

def extract_information(docs):
    print(f"Retrieved docs on inference.py: {docs}")
