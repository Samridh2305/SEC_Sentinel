from generation.answer_generator import AnswerGenerator
from retrieval.vector_retriever import VectorRetriever


class AnswerService:

    def __init__(
        self,
        retriever: VectorRetriever,
        answer_generator: AnswerGenerator
    ):
        self.retriever = retriever
        self.answer_generator = answer_generator

    def answer(
            self,
            ticker: str,
            form_type: str,
            filing_date: str,
            section:str,
            query: str
    ):
        chunks = self.retriever.retrieve(
            query=query,
            ticker=ticker,
            form_type=form_type,
            filing_date=filing_date,
            section=section,
        )
        return self.answer_generator.generate_answer(
            query=query,
            chunks=chunks
        )