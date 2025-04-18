import os
import warnings
import weaviate
from typing import List
from dotenv import load_dotenv
from langchain.schema import Document
from weaviate.classes.config import Configure

warnings.filterwarnings("ignore")

load_dotenv()

def cleanup_weaviate():
    """Delete all collections from Weaviate instance"""
    with weaviate.connect_to_local() as client:
        print("Connected to Weaviate")
        
        collections = client.collections.list_all()
        print(f"Found {len(collections)} collections: {collections}")
        
        for collection_name in collections:
            print(f"Deleting collection: {collection_name}")
            client.collections.delete(collection_name)
            
        print("All collections deleted successfully")


def retrieve_documents():
    with weaviate.connect_to_local() as client:
        print("Connected to Weaviate")

        # Querying the 'DemoCollection' to retrieve stored documents
        collection = client.collections.get("DemoCollection")
        response = collection.query.near_text(
            query="A holiday film",  # The model provider integration will automatically vectorize the query
            limit=2
        )
        
        if response.objects:
            print("Retrieved documents:")
            for obj in response.objects:
                print(obj.properties["page_content"])
            return [obj.properties for obj in response.objects]
        else:
            print("No documents found.")
            return []


def embed_and_store_documents(docs: List):
    
    cleanup_weaviate()

    with weaviate.connect_to_local() as client:
        print("Creating new collection 'DemoCollection' with vectorizer config")
        client.collections.create(
            "DemoCollection",
            vectorizer_config=[
                Configure.NamedVectors.text2vec_ollama(
                    name="title_vector",
                    source_properties=["title"],
                    api_endpoint=os.environ["WEAVIATE_OLLAMA_URL"],
                    model=os.environ["EMBEDDINGS_MODEL"],
                )
            ],
        )
        print("Collection 'DemoCollection' created successfully.")

        collection = client.collections.get("DemoCollection")
        
        with collection.batch.dynamic() as batch:
            for doc in docs:
                batch.add_object(
                    properties={
                        "page_content": doc.page_content,
                    },
                )
                if batch.number_errors > 10:
                    print("Batch import stopped due to excessive errors.")
                    break

        failed_objects = collection.batch.failed_objects
        if failed_objects:
            print(f"Number of failed imports: {len(failed_objects)}")
            print(f"First failed object: {failed_objects[0]}")
        else:
            print(f"Successfully imported {len(docs)} documents.")


if __name__ == "__main__":
    
    source_objects = [
        Document(page_content="A wrongfully imprisoned man forms an inspiring friendship while finding hope and redemption in the darkest of places."),
        Document(page_content="A powerful mafia family struggles to balance loyalty, power, and betrayal in this iconic crime saga."),
        Document(page_content="Batman faces his greatest challenge as he battles the chaos unleashed by the Joker in Gotham City."),
        Document(page_content="A desperate father goes to hilarious lengths to secure the season's hottest toy for his son on Christmas Eve."),
        Document(page_content="A miserly old man is transformed after being visited by three ghosts on Christmas Eve in this timeless tale of redemption.")
    ]
    
    
    embed_and_store_documents(source_objects)
    retrieved_documents = retrieve_documents()
