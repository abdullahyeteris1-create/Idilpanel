"""Border radius tokens for the Idil design system."""


class RadiusTokens:
    """Corner radii with card standard fixed to 12 px."""

    R8 = 8
    R10 = 10
    R12 = 12
    R16 = 16

    CARD = R12
    PANEL = R16
    INPUT = R10
    BUTTON = R10


RADIUS_SCALE = {
    "8": RadiusTokens.R8,
    "10": RadiusTokens.R10,
    "12": RadiusTokens.R12,
    "16": RadiusTokens.R16,
    "card": RadiusTokens.CARD,
    "panel": RadiusTokens.PANEL,
    "input": RadiusTokens.INPUT,
    "button": RadiusTokens.BUTTON,
}
