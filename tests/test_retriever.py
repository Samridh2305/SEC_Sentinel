
from db.database import SessionLocal

from embeddings.embedder import Embedder

from retrieval.vector_retriever import (
    VectorRetriever
)


def test_retrieve_relevant_chunks():

    session = SessionLocal()

    try:

        # 1. Create embedding model

        embedder = Embedder()


        # 2. Create retriever

        retriever = VectorRetriever(
            session=session,
            embedder=embedder
        )


        # 3. Ask a question

        results = retriever.retrieve(

            query=(
                "What risks does Apple face "
                "from tariffs and international "
                "trade restrictions?"
            ),

            top_k=5
        )


        # 4. Verify results

        assert len(results) > 0

        assert len(results) <= 5


        # 5. Print results

        for result in results:

            print(
                "\n"
                "Section:",
                result.section
            )

            print(
                "Chunk:",
                result.chunk_index
            )

            print(
                "Text:",
                result.text[:500]
            )

    finally:

        session.close()

