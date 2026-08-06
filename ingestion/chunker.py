from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from models.chunk import Chunk
from models.filing_metadata import FilingMetadata


class Chunker:

    def __init__(
        self,
        chunk_size: int = 1200,
        chunk_overlap: int = 200
    ):
        self.text_splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=[
                    "\n\n",
                    "\n",
                    ". ",
                    " ",
                    ""
                ]
            )
        )

    def chunk_sections(
        self,
        sections: dict[str, str],
        metadata: FilingMetadata
    ) -> list[Chunk]:

        chunks = []

        for section_name, section_text in sections.items():

            texts = self.text_splitter.split_text(
                section_text
            )

            for chunk_index, text in enumerate(texts):

                chunk_id = (
                    f"{metadata.ticker}_"
                    f"{metadata.form_type}_"
                    f"{metadata.filing_date}_"
                    f"{section_name}_"
                    f"{chunk_index}"
                )

                chunk = Chunk(
                    id=chunk_id,
                    ticker=metadata.ticker,
                    form_type=metadata.form_type,
                    filing_date=metadata.filing_date,
                    accession_number=(
                        metadata.accession_number
                    ),
                    section=section_name,
                    chunk_index=chunk_index,
                    text=text
                )

                chunks.append(chunk)

        return chunks

