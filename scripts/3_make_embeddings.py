import faiss
import pandas as pd
from pathlib import Path
from utils import (
    read_yaml, 
    EmbeddingModel_SBERT, 
    build_faiss_index
)

def get_input_path(config: dict) -> Path:
    input_folder = Path(config["data_folder"])
    input_file = Path(config["data_file"])
    return input_folder / input_file
    
def get_and_make_output_path(config: dict) -> Path:
    output_folder = Path(config["embeddings_folder"])
    output_file = Path(config["embeddings_file"])
    output_folder.mkdir(parents=True, exist_ok=True)
    return output_folder / output_file

def main() -> None:
    config = read_yaml("config/rag_config.yaml")
    
    input_path = get_input_path(config)
    print(f"Reading data from {input_path}")
    df = pd.read_csv(input_path)
    df.fillna('', inplace=True)
    
    print("Building embeddings...")
    model = EmbeddingModel_SBERT()
    texts = df['content'].tolist()
    embeddings = model.embed(texts)
    index = build_faiss_index(embeddings)

    output_path = get_and_make_output_path(config)
    faiss.write_index(index, str(output_path))
    print(f"Saved embeddings to {output_path}")

if __name__ == "__main__":
    main()