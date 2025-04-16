import os
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings

load_dotenv()


def getEmbeddings():
    embeddings = OllamaEmbeddings(
        model=os.environ["EMBEDDINGS_MODEL"]
    )
    
    print(embeddings)


if __name__ == "__main__":
    print("Run from vector embedding python file")
    
    print(getEmbeddings())