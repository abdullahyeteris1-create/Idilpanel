"""Typography tokens for the Idil design system."""


class TypographyTokens:
    """Poppins based type scale from docs/09-Design-System.md."""

    FONT_FAMILY = "Poppins"

    H1_WEIGHT = 700
    H1_MIN = 32
    H1_MAX = 36

    H2_WEIGHT = 700
    H2_MIN = 24
    H2_MAX = 28

    H3_WEIGHT = 600
    H3_MIN = 18
    H3_MAX = 22

    BODY_WEIGHT = 400
    BODY_MIN = 14
    BODY_MAX = 16

    CAPTION_WEIGHT = 400
    CAPTION_MIN = 12
    CAPTION_MAX = 13

    BUTTON_WEIGHT = 600
    BUTTON_MIN = 14
    BUTTON_MAX = 16


TYPE_SCALE = {
    "h1": {
        "weight": TypographyTokens.H1_WEIGHT,
        "min_size": TypographyTokens.H1_MIN,
        "max_size": TypographyTokens.H1_MAX,
    },
    "h2": {
        "weight": TypographyTokens.H2_WEIGHT,
        "min_size": TypographyTokens.H2_MIN,
        "max_size": TypographyTokens.H2_MAX,
    },
    "h3": {
        "weight": TypographyTokens.H3_WEIGHT,
        "min_size": TypographyTokens.H3_MIN,
        "max_size": TypographyTokens.H3_MAX,
    },
    "body": {
        "weight": TypographyTokens.BODY_WEIGHT,
        "min_size": TypographyTokens.BODY_MIN,
        "max_size": TypographyTokens.BODY_MAX,
    },
    "caption": {
        "weight": TypographyTokens.CAPTION_WEIGHT,
        "min_size": TypographyTokens.CAPTION_MIN,
        "max_size": TypographyTokens.CAPTION_MAX,
    },
    "button": {
        "weight": TypographyTokens.BUTTON_WEIGHT,
        "min_size": TypographyTokens.BUTTON_MIN,
        "max_size": TypographyTokens.BUTTON_MAX,
    },
    "page_title": {
        "weight": TypographyTokens.H1_WEIGHT,
        "min_size": TypographyTokens.H1_MIN,
        "max_size": TypographyTokens.H1_MAX,
    },
    "card_title": {
        "weight": TypographyTokens.H3_WEIGHT,
        "min_size": TypographyTokens.H3_MIN,
        "max_size": TypographyTokens.H3_MAX,
    },
    "subtitle": {
        "weight": TypographyTokens.H2_WEIGHT,
        "min_size": TypographyTokens.H2_MIN,
        "max_size": TypographyTokens.H2_MAX,
    },
    "small": {
        "weight": TypographyTokens.CAPTION_WEIGHT,
        "min_size": TypographyTokens.CAPTION_MIN,
        "max_size": TypographyTokens.CAPTION_MAX,
    },
}
