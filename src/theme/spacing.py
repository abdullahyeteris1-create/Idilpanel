"""Spacing scale tokens for the Idil design system."""


class SpacingTokens:
    """4-based spacing system defined in docs/09-Design-System.md."""

    S4 = 4
    S8 = 8
    S12 = 12
    S16 = 16
    S20 = 20
    S24 = 24
    S32 = 32
    S40 = 40

    XS = S4
    SM = S8
    MD = S16
    CARD = S20
    LG = S24
    XL = S32


SPACING_SCALE = {
    "4": SpacingTokens.S4,
    "8": SpacingTokens.S8,
    "12": SpacingTokens.S12,
    "16": SpacingTokens.S16,
    "20": SpacingTokens.S20,
    "24": SpacingTokens.S24,
    "32": SpacingTokens.S32,
    "40": SpacingTokens.S40,
    "xs": SpacingTokens.XS,
    "sm": SpacingTokens.SM,
    "md": SpacingTokens.MD,
    "card": SpacingTokens.CARD,
    "lg": SpacingTokens.LG,
    "xl": SpacingTokens.XL,
}
