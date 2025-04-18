import os
import time
import weaviate
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

TEMPERATURE = float(os.environ["TEMPERATURE"])
MODEL = os.environ["INFERENCE_MODEL"]
BASE_URL = os.environ["BASE_URL"]

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

def retrieve_documents(question: str):

    with weaviate.connect_to_local() as client:
        collection = client.collections.get("DemoCollection")
        response = collection.query.near_text(
            query=question,
            limit=1
        )

        if response.objects:
            results = [obj.properties["page_content"] for obj in response.objects]
            return results
        else:
            print("No documents found.")
            return []


def rag_workflow(question:str,model_class:Type[BaseModel]):
    
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
            "context": RunnableLambda(lambda q: retrieve_documents(q)),
            "question": RunnablePassthrough(),
            "format_instruction": RunnableLambda(lambda _: format_instruction)
        }
        | prompt
        | llm
        | parser
    )

    return rag_chain.invoke(question,config={"callbacks":[langfuse_handler]})


def extract_information():

    questions_and_models = [
        ("What is the SHINJING AUTO PARTS SDN. BHD. information?", BorrowerInformation), 
        ("What is the bank information?", BankInformation), 
        ("What is the loan information?", LoanInformation),
        ("What is the facility information?", FacilityInformation),
        ("What is the property information?", PropertyInformation),
        ("Formulate is the title description", TitleInformation),
        ("What is the Guarantees information?", GuarantorInformation), 
        ("What is the law firm information?", LawFirmInformation),
    ]

    extracted_information = {}

    start_time = time.time()

    for question, model in tqdm(questions_and_models,desc="Extracting information..."):
        extracted_information.update(rag_workflow(question, model))

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Total time taken for LLM inferencing in seconds: {elapsed_time:.2f} seconds")

    minutes, seconds = divmod(elapsed_time, 60)
    print(f"Total time taken for LLM inferencing in minutes and seconds: {int(minutes)} minutes and {seconds:.2f} seconds")
    
    return(extracted_information)
