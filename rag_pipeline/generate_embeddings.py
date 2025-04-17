import os
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings


def getEmbeddings():
    embeddings = OllamaEmbeddings(
        model=os.environ["EMBEDDINGS_MODEL"],
        base_url=os.environ["BASE_URL"]
    )
    
    print(embeddings)


if __name__ == "__main__":
    
    load_dotenv()
    
    print("Run from vector embedding python file")
    print(getEmbeddings())