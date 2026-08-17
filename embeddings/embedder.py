from sentence_transformers import SentenceTransformer
from common.logger import logger
from exceptions.custom_exceptions import ProcessingException
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

        try:
            embeddings = self.model.encode(texts, normalize_embeddings=True)
        except Exception as exc:
            logger.exception("Could not embed filing chunks")
            raise ProcessingException("Could not embed filing chunks.") from exc

        for chunk,embedding in zip(chunks, embeddings):
            chunk.embedding = (embedding.tolist())

        return chunks

    def embed_query(
            self,
            query: str
    ) -> list[float]:
        try:
            embedding = self.model.encode(
                query,
                normalize_embeddings=True
            )
        except Exception as exc:
            logger.exception("Could not embed query")
            raise ProcessingException("Could not embed query.") from exc

        return embedding.tolist()


