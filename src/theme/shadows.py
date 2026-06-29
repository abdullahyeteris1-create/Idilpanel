"""Shadow tokens for the Idil design system."""

import flet as ft


class ShadowTokens:
    """Soft and low-density elevation shadow."""

    COLOR = "#1E293B1F"
    BLUR_RADIUS = 20
    SPREAD_RADIUS = 0
    OFFSET_X = 0
    OFFSET_Y = 6


CARD_SHADOW = ft.BoxShadow(
    color=ShadowTokens.COLOR,
    blur_radius=ShadowTokens.BLUR_RADIUS,
    spread_radius=ShadowTokens.SPREAD_RADIUS,
    offset=ft.Offset(ShadowTokens.OFFSET_X, ShadowTokens.OFFSET_Y),
)

SHADOWS = {
    "card": CARD_SHADOW,
}
