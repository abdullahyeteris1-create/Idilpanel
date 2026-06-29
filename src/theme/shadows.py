"""Shadow tokens for the Idil design system."""

import flet as ft


class ShadowTokens:
    """Soft and low-density elevation shadow."""

    CARD_COLOR = "#0F172A14"
    CARD_BLUR_RADIUS = 10
    CARD_SPREAD_RADIUS = 0
    CARD_OFFSET_X = 0
    CARD_OFFSET_Y = 2

    HOVER_COLOR = "#0F172A1F"
    HOVER_BLUR_RADIUS = 14
    HOVER_SPREAD_RADIUS = 0
    HOVER_OFFSET_X = 0
    HOVER_OFFSET_Y = 4


CARD_SHADOW = ft.BoxShadow(
    color=ShadowTokens.CARD_COLOR,
    blur_radius=ShadowTokens.CARD_BLUR_RADIUS,
    spread_radius=ShadowTokens.CARD_SPREAD_RADIUS,
    offset=ft.Offset(ShadowTokens.CARD_OFFSET_X, ShadowTokens.CARD_OFFSET_Y),
)

HOVER_SHADOW = ft.BoxShadow(
    color=ShadowTokens.HOVER_COLOR,
    blur_radius=ShadowTokens.HOVER_BLUR_RADIUS,
    spread_radius=ShadowTokens.HOVER_SPREAD_RADIUS,
    offset=ft.Offset(ShadowTokens.HOVER_OFFSET_X, ShadowTokens.HOVER_OFFSET_Y),
)

SHADOWS = {
    "card": CARD_SHADOW,
    "hover": HOVER_SHADOW,
}
