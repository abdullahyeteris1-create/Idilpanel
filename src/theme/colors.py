"""Central color tokens for the Idil design system."""


class ColorTokens:
    """Semantic palette mapped from docs/09-Design-System.md."""

    PRIMARY = "#1E3A8A"
    SECONDARY = "#14B8A6"
    SUCCESS = "#22C55E"
    WARNING = "#F59E0B"
    DANGER = "#EF4444"
    PURPLE = "#8B5CF6"
    PASSIVE = "#64748B"
    BACKGROUND = "#F8FAFC"
    SURFACE = "#FFFFFF"
    BORDER = "#E2E8F0"

    TEXT_PRIMARY = "#0F172A"
    TEXT_SECONDARY = "#334155"
    BORDER_NEUTRAL = BORDER


SEMANTIC_COLORS = {
    "primary": ColorTokens.PRIMARY,
    "secondary": ColorTokens.SECONDARY,
    "success": ColorTokens.SUCCESS,
    "warning": ColorTokens.WARNING,
    "danger": ColorTokens.DANGER,
    "purple": ColorTokens.PURPLE,
    "passive": ColorTokens.PASSIVE,
    "background": ColorTokens.BACKGROUND,
    "surface": ColorTokens.SURFACE,
    "border": ColorTokens.BORDER,
    "text_primary": ColorTokens.TEXT_PRIMARY,
    "text_secondary": ColorTokens.TEXT_SECONDARY,
    "border_neutral": ColorTokens.BORDER_NEUTRAL,
}


STATUS_BADGE_TONES = {
    "Aktif": ColorTokens.SUCCESS,
    "Pasif": ColorTokens.WARNING,
    "Tamamlandi": ColorTokens.PRIMARY,
}
