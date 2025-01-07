import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
from tqdm import tqdm

def build_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatIP:
    """Build a FAISS index for a set of embeddings.
    """
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    return index

class EmbeddingModel_SBERT:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)


    def embed(self, texts: list[str], show_progress_bar: bool = True) -> np.ndarray:
        """Generate normalized embeddings for a list of texts.
        """
        embeddings = self.model.encode(texts, show_progress_bar=show_progress_bar)
        embeddings_norm = normalize(embeddings, axis=1)
        return embeddings_norm
    

def retrieve_similar_texts(
        query: str, 
        model: EmbeddingModel_SBERT, 
        index: faiss.IndexFlatIP, 
        df: pd.DataFrame, 
        k: int = 5) -> pd.DataFrame:
    """
    Retrieve the top k texts similar to the query using FAISS.
    """
    qe = model.embed([query])
    qe_norm = normalize(qe, axis=1)
    distances, idx = index.search(np.array(qe_norm), k)
    retrieved_data = df.iloc[idx[0]].copy()
    retrieved_data['similarity_score'] = 1 - distances[0]

    return retrieved_data
