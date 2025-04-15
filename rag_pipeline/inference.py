import os
import time
from tqdm import tqdm
from dotenv import load_dotenv
from typing import Type
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnablePassthrough
from langfuse.callback import CallbackHandler
from rag_pipeline.detail_information import (
                                                BorrowerInformation,
                                                BankInformation,
                                                LoanInformation,
                                                GuarantorInformation,
                                                LawFirmInformation,
                                                TitleInformation,
                                                PropertyInformation,
                                                FacilityInformation,
                                            )

load_dotenv()

TEMPERATURE = 0.0
MODEL = 'deepseek-r1:8b'
BASE_URL = 'http://localhost:11434/'

llm = ChatOllama(temperature=TEMPERATURE,model=MODEL,base_url=BASE_URL)
results = {}


langfuse_handler = CallbackHandler(
    public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
    secret_key=os.environ["LANGFUSE_SECRET_KEY"],
    host=os.environ["LANGFUSE_URL"],
)


def read_file_content(path: str) -> str:
    """Reads content from a file and returns it as a string."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"Failed to read file: {e}"


def rag_workflow(question:str,model_class:Type[BaseModel],path:str):
    
    context = read_file_content(path)

    parser = JsonOutputParser(pydantic_object=model_class)
    format_instruction = parser.get_format_instructions()

    prompt_template = """
        You are an assistant for question-answering tasks. Use the following retrieved context to answer the question. 
        Only output the answer itself, without any additional explanation or commentary. 
        If there is no relevant information or you don't know the answer, reply with an empty string ("") or null.
        
        Question: {question}
        Context: {context}
        
        Here is your formatting instruction:
        {format_instruction}
        
        Answer:
        """
    
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    rag_chain = (
        {
            "context": RunnableLambda(lambda _: context),
            "question": RunnablePassthrough(),
            "format_instruction": RunnableLambda(lambda _: format_instruction)
        }
        | prompt
        | llm
        | parser
    )

    return rag_chain.invoke(question,config={"callbacks":[langfuse_handler]})


def extract_information(docs:list):

    context = docs

    questions_and_models = [
        ("What is the LIM PHIANG KEE @ LIM SEOW MEI information?", BorrowerInformation, "transformed_files/lo 1_page_1_extracted_transformed.txt"), 
        ("What is the bank information?", BankInformation, "transformed_files/lo 1_page_1_extracted_transformed.txt"), 
        ("What is the loan information?", LoanInformation, "transformed_files/lo 1_page_1_extracted_transformed.txt"),
        # ("What is the facility information?", FacilityInformation, "transformed_files/lo 1_page_1_extracted_transformed.txt"),
        # ("What is the property information?", PropertyInformation, "transformed_files/lo 1_page_1_extracted_transformed.txt"),
        # ("Formulate is the title description", TitleInformation, "transformed_files/lo 1_page_1_extracted_transformed.txt"),
        ("What is the Guarantees information?", GuarantorInformation, "transformed_files/lo 1_page_1_extracted_transformed.txt"), 
        ("What is the law firm information?", LawFirmInformation, "transformed_files/lo 1_page_1_extracted_transformed.txt"),
    ]

    extracted_information = {}

    start_time = time.time()

    for question, model, context in tqdm(questions_and_models,desc="Extracting information..."):
        extracted_information.update(rag_workflow(question, model, context))

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Total time taken for LLM inferencing in seconds: {elapsed_time:.2f} seconds")

    minutes, seconds = divmod(elapsed_time, 60)
    print(f"Total time taken for LLM inferencing in minutes and seconds: {int(minutes)} minutes and {seconds:.2f} seconds")
    
    return(extracted_information)
