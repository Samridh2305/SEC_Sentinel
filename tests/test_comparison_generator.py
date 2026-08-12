from db.database import SessionLocal

from embeddings.embedder import Embedder
from retrieval.vector_retriever import VectorRetriever

from generation.comparison_generator import ComparisonGenerator

from models.comparision import Comparison


def test_generate_comparison():

    session = SessionLocal()

    try:

        # 1. Create Embedder

        embedder = Embedder()

        # 2. Create Retriever

        retriever = VectorRetriever(
            session=session,
            embedder=embedder
        )

        query = (
            "Compare the risk factors related to tariffs "
            "between the two filings."
        )

        # 3. Retrieve previous filing chunks

        previous_chunks = retriever.retrieve(
            query=query,
            ticker="AAPL",
            form_type="10-K",
            filing_date="2024-09-28",
            top_k=5
        )

        # 4. Retrieve current filing chunks

        current_chunks = retriever.retrieve(
            query=query,
            ticker="AAPL",
            form_type="10-K",
            filing_date="2025-09-27",
            top_k=5
        )

        # 5. Create Comparison Generator

        generator = ComparisonGenerator()

        # 6. Generate comparison

        comparison = generator.generate_comparison(
            query=query,
            previous_chunks=previous_chunks,
            current_chunks=current_chunks,
        )

        # 7. Verify Comparison object

        assert isinstance(
            comparison,
            Comparison
        )

        # 8. Verify comparison text

        assert isinstance(
            comparison.text,
            str
        )

        assert len(
            comparison.text.strip()
        ) > 0

        # 9. Verify sources

        assert comparison.previous_sources == previous_chunks
        assert comparison.current_sources == current_chunks

        assert len(comparison.previous_sources) > 0
        assert len(comparison.current_sources) > 0

    finally:

        session.close()