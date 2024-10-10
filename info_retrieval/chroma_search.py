import pickle

import chromadb


chroma_client = chromadb.PersistentClient(path="./chroma_data")
collection = chroma_client.get_collection(name="mathtext")

with open('../data/metadata.pickle', 'rb') as f:
    metadata = pickle.load(f)

results = collection.query(
    query_texts=["prime numbers"],
    n_results=10,
)

for fn in results["ids"][0]:
    print(metadata[fn])

