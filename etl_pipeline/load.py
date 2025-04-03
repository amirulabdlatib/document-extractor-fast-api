import os
import re
from langchain_community.document_loaders import DirectoryLoader

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]

def load_files():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    transformed_dir = os.path.join(base_dir, "transformed_files")

    loader = DirectoryLoader(
        transformed_dir,
        glob="**/*.txt",
        recursive=True, 
        show_progress=True
    )

    docs = loader.load()
    docs = sorted(docs, key=lambda x: natural_sort_key(x.metadata['source']))

    print(f"Loaded {len(docs)} documents")

    print("\nAll documents in sorted order:")
    for i, doc in enumerate(docs):
        filename = os.path.basename(doc.metadata['source'])
        print(f"{i}: {filename}")


    return docs