from openai import OpenAI

from common.config import settings
from db.models.filing_chunk import FilingChunk
from models.comparision import Comparison
from prompts.comparision_prompt import (
    COMPARISON_SYSTEM_PROMPT,
    COMPARISON_PROMPT
)


class ComparisonGenerator:

    def __init__(
        self,
        model: str = "gpt-4.1-mini"
    ):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

        self.model = model


    def generate_comparison(
        self,
        query: str,
        previous_chunks: list[FilingChunk],
        current_chunks: list[FilingChunk],
    ) -> Comparison:

        previous_context = "\n\n".join(
            [
                (
                    f"Section: {chunk.section}\n"
                    f"Chunk: {chunk.chunk_index}\n"
                    f"Text: {chunk.text}"
                )
                for chunk in previous_chunks
            ]
        )

        current_context = "\n\n".join(
            [
                (
                    f"Section: {chunk.section}\n"
                    f"Chunk: {chunk.chunk_index}\n"
                    f"Text: {chunk.text}"
                )
                for chunk in current_chunks
            ]
        )

        user_prompt = COMPARISON_PROMPT.format(
            previous_context=previous_context,
            current_context=current_context,
            query=query
        )


        response = self.client.responses.create(
            model=self.model,
            instructions=COMPARISON_SYSTEM_PROMPT,
            input=user_prompt
        )

        return Comparison(
            text=response.output_text,
            previous_sources=previous_chunks,
            current_sources=current_chunks
        )

