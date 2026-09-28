from google import genai
from google.genai import types

from app.config import get_settings
from app.models import (
    ComicOutline,
    ComicStory,
    PromptRequest,
)


def _client() -> genai.Client:

    settings = get_settings()

    if not settings.gemini_api_key:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_story(
    request: PromptRequest,
    outline: ComicOutline
) -> ComicStory:

    settings = get_settings()

    # Mock mode
    if settings.mock_ai:

        return ComicStory(

            panels=[

                {
                    "panel_number": panel.panel_number,

                    "caption": (
                        f"The {request.tone.lower()} "
                        f"adventure continues."
                    ),

                    "narration": (
                        panel.scene_description
                    ),

                    "dialogue": [
                        (
                            f"{request.character_name}: "
                            "Let's see what happens next!"
                        )
                    ],
                }

                for panel in outline.panels
            ]
        )

    prompt = f"""
Write the complete story for this five-panel comic.

Character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Comic outline:

{outline.model_dump_json(indent=2)}

Requirements:

- Exactly five panels.
- Match the panel numbers.
- Every panel needs:
  - caption
  - narration
  - dialogue
- Keep story continuity.
- Make dialogue short and natural.
- Do not create extra panels.
- Keep content suitable for a general audience.
"""

    client = _client()

    response = client.models.generate_content(

        model=settings.gemini_pro_model,

        contents=prompt,

        config=types.GenerateContentConfig(

            response_mime_type="application/json",

            response_schema=ComicStory,

            temperature=0.85,
        ),
    )

    if response.parsed:

        story = response.parsed

    else:

        story = ComicStory.model_validate_json(
            response.text
        )

    story.panels.sort(
        key=lambda panel: panel.panel_number
    )

    if len(story.panels) != 5:

        raise RuntimeError(
            "Gemini returned an invalid story."
        )

    for index, panel in enumerate(
        story.panels,
        start=1
    ):

        panel.panel_number = index

    return story