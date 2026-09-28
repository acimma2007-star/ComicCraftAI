from app.models import (
    ComicOutline,
    ComicStory,
    ComicPanel,
)


def build_comic_layout(
    outline: ComicOutline,
    story: ComicStory,
    image_paths: list[str],
) -> list[ComicPanel]:

    if (
        len(outline.panels)
        != len(story.panels)
        or
        len(outline.panels)
        != len(image_paths)
    ):

        raise ValueError(
            "Outline, story and image counts "
            "must match."
        )

    story_by_number = {
        panel.panel_number: panel
        for panel in story.panels
    }

    result = []

    for (
        outline_panel,
        image_path
    ) in zip(
        outline.panels,
        image_paths
    ):

        story_panel = story_by_number[
            outline_panel.panel_number
        ]

        result.append(

            ComicPanel(

                panel_number=(
                    outline_panel.panel_number
                ),

                title=outline_panel.title,

                scene_description=(
                    outline_panel.scene_description
                ),

                image_prompt=(
                    outline_panel.image_prompt
                ),

                image_path=image_path,

                caption=story_panel.caption,

                narration=story_panel.narration,

                dialogue=story_panel.dialogue,
            )
        )

    return result