from openai import OpenAI, OpenAIError

from common.config import settings
from common.logger import logger
from db.models.filing_chunk import FilingChunk
from exceptions.custom_exceptions import ServiceException
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


        try:
            response = self.client.responses.create(
                model=self.model,
                instructions=ANSWER_SYSTEM_PROMPT,
                input=user_prompt
            )
        except OpenAIError as exc:
            logger.exception("Could not generate filing answer")
            raise ServiceException("The AI service is temporarily unavailable.") from exc

        return Answer(
            text=response.output_text,
            sources=chunks
        )

