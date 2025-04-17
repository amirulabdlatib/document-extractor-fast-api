import weaviate

def connect():
    return weaviate.connect_to_local()

def create_schema_if_not_exists(client):
    pass

def store_to_vector_db(embeddings):
    with connect() as client:
        print("Weaviate Ready:", client.is_ready())
        create_schema_if_not_exists(client)

        for item in embeddings:
            pass

if __name__ == "__main__":
    print("Run from vector database python file")
    
    with weaviate.connect_to_local() as client:
        print("Weaviate Ready:", client.is_ready())