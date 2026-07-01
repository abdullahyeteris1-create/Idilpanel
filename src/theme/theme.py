"""Central theme builder for the Idil design system."""

import flet as ft

from .colors import ColorTokens, SEMANTIC_COLORS, STATUS_BADGE_TONES
from .radius import RADIUS_SCALE
from .shadows import SHADOWS
from .spacing import SPACING_SCALE
from .typography import TYPE_SCALE, TypographyTokens


class IdilTheme:
    """Single source of truth for application theme tokens."""

    DARK_MODE_ENABLED = False

    @staticmethod
    def build_light_theme() -> ft.Theme:
        return ft.Theme(
            color_scheme_seed=ColorTokens.PRIMARY,
            font_family=TypographyTokens.FONT_FAMILY,
        )

    @staticmethod
    def apply_to_page(page: ft.Page) -> None:
        page.theme_mode = ft.ThemeMode.LIGHT
        page.theme = IdilTheme.build_light_theme()
        page.bgcolor = ColorTokens.BACKGROUND


THEME_TOKENS = {
    "colors": SEMANTIC_COLORS,
    "status_badges": STATUS_BADGE_TONES,
    "typography": TYPE_SCALE,
    "spacing": SPACING_SCALE,
    "radius": RADIUS_SCALE,
    "shadows": SHADOWS,
    "dark_mode_enabled": IdilTheme.DARK_MODE_ENABLED,
}
