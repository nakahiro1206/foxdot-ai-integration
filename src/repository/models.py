from pydantic import BaseModel, Field


class CodeEntity(BaseModel):
    name: str
    language: str
    code_content: str
    intent_description: str


class CodeEntitySearchResult(BaseModel):
    """A single search hit with similarity metadata."""

    id: int
    distance: float = Field(description="Cosine similarity score")
    entity: CodeEntity

    @classmethod
    def from_hit(cls, hit: dict) -> "CodeEntitySearchResult":
        entity_data = hit["entity"]
        return cls(
            id=hit["id"],
            distance=hit["distance"],
            entity=CodeEntity(
                name=entity_data["entity_name"],
                language=entity_data["language"],
                code_content=entity_data["code_content"],
                intent_description=entity_data["intent_description"],
            ),
        )


class CodeEntitySummary(BaseModel):
    """Lightweight view returned by list_all (no code_content)."""

    id: int
    name: str
    language: str
    intent_description: str

    @classmethod
    def from_row(cls, row: dict) -> "CodeEntitySummary":
        return cls(
            id=row["id"],
            name=row["entity_name"],
            language=row["language"],
            intent_description=row["intent_description"],
        )
