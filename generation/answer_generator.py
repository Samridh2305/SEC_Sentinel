from openai import OpenAI

from common.config import settings
from db.models.filing_chunk import FilingChunk
from models.answer import Answer
from prompts.answer_prompt import (
    ANSWER_PROMPT,
    ANSWER_SYSTEM_PROMPT
)


class AnswerGenerator:

    def __init__(
        self,
        model: str = "gpt-4.1-mini"
    ):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

        self.model = model

    def generate_answer(
        self,
        query: str,
        chunks: list[FilingChunk]
    ) -> Answer:

        context = "\n\n".join(
            [
                (
                    f"Section: {chunk.section}\n"
                    f"Chunk: {chunk.chunk_index}\n"
                    f"Text: {chunk.text}"
                )
                for chunk in chunks
            ]
        )
        user_prompt = ANSWER_PROMPT.format(
            context=context,
            query=query
        )


        response = self.client.responses.create(
            model=self.model,
            instructions=ANSWER_SYSTEM_PROMPT,
            input=user_prompt
        )

        return Answer(
            text=response.output_text,
            sources=chunks
        )

