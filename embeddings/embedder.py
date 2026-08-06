from sentence_transformers import SentenceTransformer
from models.chunk import Chunk

class Embedder:
    def __init__(
            self,
            model_name: str = "BAAI/bge-base-en-v1.5"
    ):
        self.model = SentenceTransformer(model_name)

    def embed_chunks(
            self,
            chunks: list[Chunk]
            ) -> list[Chunk]:

        texts = [
            chunk.text
            for chunk in chunks
        ]

        embeddings = self.model.encode(texts, normalize_embeddings=True)

        for chunk,embedding in zip(chunks, embeddings):
            chunk.embedding = (embedding.tolist())

        return chunks

    def embed_query(
            self,
            query: str
    ) -> list[float]:
        embedding = self.model.encode(
            query,
            normalize_embeddings=True
        )

        return embedding.tolist()


