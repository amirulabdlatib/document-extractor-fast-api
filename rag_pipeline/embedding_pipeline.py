import weaviate
from weaviate.classes.config import Configure

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

if __name__ == "__main__":
    cleanup_weaviate()