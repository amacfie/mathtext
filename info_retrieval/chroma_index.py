import pathlib
import pickle

import chromadb
import tqdm


if __name__ == '__main__':
    chroma_client = chromadb.PersistentClient(path="./chroma_data")
    try:
        chroma_client.delete_collection(name="mathtext")
    except ValueError:
        pass
    collection = chroma_client.create_collection(name="mathtext")

    with open('../data/metadata.pickle', 'rb') as f:
        metadata = pickle.load(f)

    for key in tqdm.tqdm(metadata.keys(), total=len(metadata)):
        path = pathlib.Path("../data/documents") / key
        collection.add(documents=[path.read_text()], ids=[key])

