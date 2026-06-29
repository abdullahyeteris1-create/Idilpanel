"""Typography tokens for the Idil design system."""


class TypographyTokens:
    """Poppins based type scale from docs/09-Design-System.md."""

    FONT_FAMILY = "Poppins"

    PAGE_TITLE_WEIGHT = 700
    PAGE_TITLE_MIN = 28
    PAGE_TITLE_MAX = 36

    CARD_TITLE_WEIGHT = 600
    CARD_TITLE_MIN = 18
    CARD_TITLE_MAX = 22

    SUBTITLE_WEIGHT = 600
    SUBTITLE_MIN = 16
    SUBTITLE_MAX = 20

    BODY_WEIGHT = 400
    BODY_MIN = 14
    BODY_MAX = 16

    SMALL_WEIGHT = 400
    SMALL_MIN = 12
    SMALL_MAX = 13

    BUTTON_WEIGHT = 600
    BUTTON_MIN = 14
    BUTTON_MAX = 16


TYPE_SCALE = {
    "page_title": {
        "weight": TypographyTokens.PAGE_TITLE_WEIGHT,
        "min_size": TypographyTokens.PAGE_TITLE_MIN,
        "max_size": TypographyTokens.PAGE_TITLE_MAX,
    },
    "card_title": {
        "weight": TypographyTokens.CARD_TITLE_WEIGHT,
        "min_size": TypographyTokens.CARD_TITLE_MIN,
        "max_size": TypographyTokens.CARD_TITLE_MAX,
    },
    "subtitle": {
        "weight": TypographyTokens.SUBTITLE_WEIGHT,
        "min_size": TypographyTokens.SUBTITLE_MIN,
        "max_size": TypographyTokens.SUBTITLE_MAX,
    },
    "body": {
        "weight": TypographyTokens.BODY_WEIGHT,
        "min_size": TypographyTokens.BODY_MIN,
        "max_size": TypographyTokens.BODY_MAX,
    },
    "small": {
        "weight": TypographyTokens.SMALL_WEIGHT,
        "min_size": TypographyTokens.SMALL_MIN,
        "max_size": TypographyTokens.SMALL_MAX,
    },
    "button": {
        "weight": TypographyTokens.BUTTON_WEIGHT,
        "min_size": TypographyTokens.BUTTON_MIN,
        "max_size": TypographyTokens.BUTTON_MAX,
    },
}
