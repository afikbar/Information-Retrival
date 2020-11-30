import os
import sys

from BooleanRetrieval import BooleanRetrieval
from InvertedIndex import InvertedIndex


def main(docs_path: str, query_path: str):
    docs_files = os.scandir(docs_path)

    inv_idx = InvertedIndex()
    print(f"Indexing {docs_path}...")
    for file in docs_files:
        try:
            inv_idx.parse_file(file.path)
        except Exception as e:
            print(f"Error at {file.name}:\n\t{e}")
            raise e

    inv_idx.finalize()
    print("Inverted Index is built.")
    print("Fetching queries...")
    with open(query_path, 'r') as f:
        with open("Task_2.txt", 'w') as o:
            o.write('\n'.join([BooleanRetrieval(inv_idx, q) for q in f]))
    print("Done querying.")
    print("Collection statistics...")
    with open("Task_3.txt", 'w') as f:
        terms = list(inv_idx.index.keys())

        f.write(f"Terms with highest document frequency:\n{terms[:10]}\n")
        f.write(f"Terms with lowest document frequency:\n{terms[-10:]}")
    print("Done.")


if __name__ == '__main__':
    main(*sys.argv[1:])
