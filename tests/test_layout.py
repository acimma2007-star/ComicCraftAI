from app.models import (
    ComicOutline,
    ComicStory,
    PanelOutline,
    PanelStory,
)

from app.services.layout_builder import (
    build_comic_layout
)


def test_build_layout():

    outline = ComicOutline(

        panels=[

            PanelOutline(

                panel_number=i,

                title=f"Panel {i}",

                scene_description="Test scene",

                image_prompt="Test image"

            )

            for i in range(1, 6)

        ]
    )


    story = ComicStory(

        panels=[

            PanelStory(

                panel_number=i,

                caption="Test caption",

                narration="Test narration",

                dialogue=["Hello"]

            )

            for i in range(1, 6)

        ]
    )


    images = [

        f"/static/panels/panel-{i}.png"

        for i in range(1, 6)

    ]


    layout = build_comic_layout(

        outline,

        story,

        images

    )


    assert len(layout) == 5

    assert layout[2].panel_number == 3

    assert layout[4].dialogue == [
        "Hello"
    ]