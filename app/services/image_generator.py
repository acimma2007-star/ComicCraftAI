import re
from pathlib import Path

from PIL import Image, ImageDraw

from app.config import get_settings


def _safe_name(
    prompt: str,
    panel_number: int
) -> str:

    slug = re.sub(
        r"[^a-zA-Z0-9]+",
        "-",
        prompt
    ).strip("-").lower()

    slug = slug[:60] or "panel"

    return (
        f"panel-{panel_number}-{slug}.png"
    )


def _placeholder(
    prompt: str,
    path: Path,
    panel_number: int
):

    image = Image.new(
        "RGB",
        (1024, 768),
        "white"
    )

    draw = ImageDraw.Draw(image)

    draw.rectangle(
        (20, 20, 1004, 748),
        outline="black",
        width=6
    )

    draw.text(
        (60, 60),
        f"ComicCraft - Panel {panel_number}",
        fill="black"
    )

    words = prompt.split()

    lines = []

    current_line = ""

    for word in words:

        if (
            len(current_line)
            + len(word)
            + 1
            > 65
        ):

            lines.append(current_line)

            current_line = word

        else:

            current_line = (
                f"{current_line} {word}"
            ).strip()

    if current_line:

        lines.append(current_line)

    y = 130

    for line in lines[:12]:

        draw.text(
            (60, y),
            line,
            fill="black"
        )

        y += 42

    image.save(
        path,
        format="PNG"
    )


def generate_image(
    prompt: str,
    panel_number: int
) -> str:

    settings = get_settings()

    filename = _safe_name(
        prompt,
        panel_number
    )

    output_path = (
        settings.panel_dir
        / filename
    )

    # Development placeholder
    if (
        settings.image_provider.lower()
        == "placeholder"
    ):

        _placeholder(
            prompt,
            output_path,
            panel_number
        )

        return (
            f"/static/panels/{filename}"
        )

    token = settings.effective_hf_token

    if not token:

        raise RuntimeError(
            "HF_TOKEN or HF_API_KEY "
            "is required."
        )

    try:

        from huggingface_hub import (
            InferenceClient
        )

        client = InferenceClient(
            provider="auto",
            api_key=token
        )

        image = client.text_to_image(

            prompt=prompt,

            model=settings.hf_image_model
        )

        image.save(output_path)

    except Exception as exc:

        raise RuntimeError(
            f"Image generation failed: {exc}"
        ) from exc

    return (
        f"/static/panels/{filename}"
    )