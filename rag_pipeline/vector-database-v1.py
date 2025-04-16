import weaviate



if __name__ == "__main__":
    print("Run from vector database python file")
    
    with weaviate.connect_to_local() as client:
        print("Weaviate Ready:", client.is_ready())