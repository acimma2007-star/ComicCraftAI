from google import genai
from google.genai import types

from app.config import get_settings
from app.models import (
    ComicOutline,
    PanelOutline,
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


def generate_outline(
    request: PromptRequest
) -> ComicOutline:

    settings = get_settings()

    # Mock mode
    if settings.mock_ai:

        return ComicOutline(
            panels=[
                PanelOutline(
                    panel_number=i,

                    title=f"Panel {i}",

                    scene_description=(
                        f"{request.character_name} "
                        f"moves the story forward "
                        f"in the {request.setting}."
                    ),

                    image_prompt=(
                        f"{request.art_style} comic panel, "
                        f"{request.character_name}, "
                        f"{request.setting}, "
                        f"cinematic composition"
                    ),
                )

                for i in range(1, 6)
            ]
        )

    prompt = f"""
Create a coherent five-panel comic outline.

Story idea:
{request.story_prompt}

Main character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Requirements:

- Exactly five panels.
- Keep the same main character throughout.
- Panel 1 establishes the situation.
- Panels 2, 3 and 4 develop the story.
- Panel 5 gives a satisfying ending.
- Describe visible actions and environments.
- Create detailed image prompts.
- Keep the content suitable for a general audience.
"""

    client = _client()

    response = client.models.generate_content(

        model=settings.gemini_flash_model,

        contents=prompt,

        config=types.GenerateContentConfig(

            response_mime_type="application/json",

            response_schema=ComicOutline,

            temperature=0.9,
        ),
    )

    if response.parsed:

        outline = response.parsed

    else:

        outline = ComicOutline.model_validate_json(
            response.text
        )

    outline.panels.sort(
        key=lambda panel: panel.panel_number
    )

    if len(outline.panels) != 5:

        raise RuntimeError(
            "Gemini returned an invalid number of panels."
        )

    for index, panel in enumerate(
        outline.panels,
        start=1
    ):

        panel.panel_number = index

    return outline