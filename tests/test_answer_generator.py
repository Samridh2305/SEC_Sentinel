from db.database import SessionLocal

from embeddings.embedder import Embedder

from retrieval.vector_retriever import (
    VectorRetriever
)

from models.answer import Answer

from generation.answer_generator import (
    AnswerGenerator
)


def test_generate_answer():

    session = SessionLocal()

    try:

        # 1. Create Embedder

        embedder = Embedder()


        # 2. Create Retriever

        retriever = VectorRetriever(
            session=session,
            embedder=embedder
        )


        # 3. Retrieve relevant chunks

        query = (
            "What risks does Apple face "
            "from tariffs and international "
            "trade restrictions?"
        )

        chunks = retriever.retrieve(
            query=query,
            top_k=5
        )


        # 4. Create Answer Generator

        generator = AnswerGenerator()


        # 5. Generate answer

        answer = generator.generate_answer(
            query=query,
            chunks=chunks
        )


        # 6. Check Answer object

        assert isinstance(
            answer,
            Answer
        )


        # 7. Check answer text

        assert isinstance(
            answer.text,
            str
        )

        assert len(
            answer.text.strip()
        ) > 0


        # 8. Check sources

        assert len(
            answer.sources
        ) > 0


        # 9. Verify sources are
        #    the retrieved chunks

        assert answer.sources == chunks


    finally:

        session.close()

