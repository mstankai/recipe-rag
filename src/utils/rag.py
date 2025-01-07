import faiss
import numpy as np

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
    
