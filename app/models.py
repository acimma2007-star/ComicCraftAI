from pydantic import BaseModel, Field


class PanelOutline(BaseModel):

    panel_number: int = Field(
        ge=1,
        le=5
    )

    title: str

    scene_description: str

    image_prompt: str


class ComicOutline(BaseModel):

    panels: list[PanelOutline] = Field(
        min_length=5,
        max_length=5
    )


class PanelStory(BaseModel):

    panel_number: int = Field(
        ge=1,
        le=5
    )

    caption: str

    narration: str

    dialogue: list[str] = Field(
        default_factory=list
    )


class ComicStory(BaseModel):

    panels: list[PanelStory] = Field(
        min_length=5,
        max_length=5
    )


class PromptRequest(BaseModel):

    story_prompt: str = Field(
        min_length=5,
        max_length=2000
    )

    character_name: str = Field(
        min_length=1,
        max_length=100
    )

    setting: str = Field(
        min_length=1,
        max_length=100
    )

    tone: str = Field(
        min_length=1,
        max_length=50
    )

    art_style: str = Field(
        min_length=1,
        max_length=100
    )


class ComicPanel(BaseModel):

    panel_number: int

    title: str

    scene_description: str

    image_prompt: str

    image_path: str

    caption: str

    narration: str

    dialogue: list[str]


class ComicResponse(BaseModel):

    panels: list[ComicPanel]

    pdf_path: str