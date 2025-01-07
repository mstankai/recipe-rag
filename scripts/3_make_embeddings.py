import faiss
import pandas as pd
from pathlib import Path
from utils import (
    read_yaml, 
    EmbeddingModel_SBERT, 
    build_faiss_index
)

def get_input_path(data_config: dict) -> Path:
    input_folder = Path(data_config["output_folder"])
    input_file = Path(data_config["output_file"] + '_rag_input.csv')
    return input_folder / input_file
    
def get_and_make_output_path(rag_config: dict) -> Path:
    output_folder = Path(rag_config["embeddings_folder"])
    output_file = Path(rag_config["embeddings_file"])
    output_folder.mkdir(parents=True, exist_ok=True)
    return output_folder / output_file

def main() -> None:
    data_config = read_yaml("config/data_config.yaml")
    rag_config = read_yaml("config/rag_config.yaml")
    
    input_path = get_input_path(data_config)
    print(f"Reading data from {input_path}")
    df = pd.read_csv(input_path)
    df.fillna('', inplace=True)
    
    print("Building embeddings...")
    model = EmbeddingModel_SBERT()
    texts = df['content'].tolist()
    embeddings = model.embed(texts)
    index = build_faiss_index(embeddings)

    output_path = get_and_make_output_path(rag_config)
    faiss.write_index(index, str(output_path))
    print(f"Saved embeddings to {output_path}")

if __name__ == "__main__":
    main()