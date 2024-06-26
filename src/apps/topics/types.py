import enum


class ContactType(str, enum.Enum):
    """Subscription contact type."""

    EMAIL = "Email"
    DISCORD = "Discord"
    TELEGRAM = "Telegram"

    @classmethod
    def choices(cls) -> dict:
        """Return types as dict."""
        return {member.value: member.value for member in cls}
