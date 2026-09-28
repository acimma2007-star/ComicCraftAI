from pathlib import Path
from uuid import uuid4

from fpdf import FPDF

from app.config import get_settings
from app.models import ComicPanel


def _local_image_path(
    web_path: str
) -> Path:

    settings = get_settings()

    relative = (
        web_path
        .removeprefix("/static/")
        .lstrip("/")
    )

    return (
        settings.static_dir
        / relative
    )


def save_pdf(
    layout: list[ComicPanel]
) -> str:

    settings = get_settings()

    filename = (
        f"comic-{uuid4().hex[:10]}.pdf"
    )

    output = (
        settings.export_dir
        / filename
    )

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4"
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    for panel in layout:

        pdf.add_page()

        pdf.set_font(
            "Helvetica",
            "B",
            18
        )

        pdf.cell(
            0,
            10,
            (
                f"Panel {panel.panel_number}: "
                f"{panel.title}"
            ),
            new_x="LMARGIN",
            new_y="NEXT"
        )

        image = _local_image_path(
            panel.image_path
        )

        if image.exists():

            pdf.image(
                str(image),
                x=15,
                y=30,
                w=180,
                h=115,
                keep_aspect_ratio=True
            )

        pdf.set_y(152)

        pdf.set_font(
            "Helvetica",
            "I",
            10
        )

        pdf.multi_cell(
            180,
            6,
            f"Caption:{panel.caption}"
        )

        pdf.ln(3)

        pdf.set_font(
            "Helvetica",
            "B",
            11
        )

        pdf.multi_cell(
            0,
            6,
            f"Caption: {panel.caption}"
        )

        pdf.ln(2)

        pdf.set_font(
            "Helvetica",
            "",
            11
        )

        pdf.multi_cell(
            0,
            6,
            panel.narration
        )

        if panel.dialogue:

            pdf.ln(2)

            pdf.set_font(
                "Helvetica",
                "B",
                11
            )

            pdf.multi_cell(
                180,
                6,
                "Dialogue:"
            )

            pdf.set_font(
                "Helvetica",
                "",
                11
            )

            for line in panel.dialogue:

                pdf.multi_cell(
                   180,
                    6,
                    f"- {line}"
                )

    pdf.output(str(output))

    return (
        f"/static/exports/{filename}"
    )