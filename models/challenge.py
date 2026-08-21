from pydantic import BaseModel, Field

class Challenge(BaseModel):
    topic: str = Field(
        description="The topic of the reading passage."
    )

    content: str = Field(
        description="The reading passage generated for the user."
    )

    word_count: int = Field(
        description="The actual number of words in the generated passage."
    )

    difficulty: str = Field(
        description="The difficulty level of the passage."
    )

    key_concepts: list[str] = Field(
        description="The important concepts from the passage that the user should ideally remember."
    )

