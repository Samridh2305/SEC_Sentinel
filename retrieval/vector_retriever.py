from datetime import datetime

from sqlalchemy.orm import Session

from common.logger import logger
from db.models.filing_chunk import FilingChunk
from embeddings.embedder import Embedder
from exceptions.custom_exceptions import DatabaseException


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
        filing_date: str | None = None,
        section: str | None = None,
        top_k: int = 5
    ) -> list[FilingChunk]:

        # 1. Convert user question into embedding
        query_embedding = self.embedder.embed_query(
            query
        )

        # 2. Start database query
        db_query = self.session.query(FilingChunk)

        # 3.  ticker filter
        if ticker:
            db_query = db_query.filter(
                FilingChunk.ticker == ticker
            )

        # 4. form_type filter
        if form_type:
            db_query = db_query.filter(
                FilingChunk.form_type == form_type
            )

        #5. filing_date filler
        if filing_date:
            filing_date = datetime.strptime(
                filing_date,
                "%Y-%m-%d"
            ).date()
            db_query = db_query.filter(
                FilingChunk.filing_date == filing_date
            )

        # 6. filing_date filler
        if section:
            db_query = db_query.filter(
                FilingChunk.section == section
            )

        try:
            # 7. Perform cosine similarity search
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
        except Exception as exc:
            logger.exception("Could not retrieve filing chunks")
            raise DatabaseException() from exc

        # 8. Return most relevant chunks
        return results
