from sqlalchemy.orm import Session

from db.models.filing_chunk import FilingChunk
from embeddings.embedder import Embedder


class VectorRetriever:

    def __init__(
        self,
        session: Session,
        embedder: Embedder
    ):
        self.session = session
        self.embedder = embedder

    def retrieve(
        self,
        query: str,
        ticker: str | None = None,
        form_type: str | None = None,
        top_k: int = 5
    ) -> list[FilingChunk]:

        # 1. Convert user question into embedding
        query_embedding = self.embedder.embed_query(
            query
        )

        # 2. Start database query
        db_query = self.session.query(FilingChunk)

        # 3. Apply optional ticker filter
        if ticker:
            db_query = db_query.filter(
                FilingChunk.ticker == ticker
            )

        # 4. Apply optional form type filter
        if form_type:
            db_query = db_query.filter(
                FilingChunk.form_type == form_type
            )

        # 5. Perform cosine similarity search
        results = (
            db_query
            .order_by(
                FilingChunk.embedding.cosine_distance(
                    query_embedding
                )
            )
            .limit(top_k)
            .all()
        )

        # 6. Return most relevant chunks
        return results