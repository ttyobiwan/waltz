import enum


class ContactType(enum.Enum):
    """Subscription contact type."""

    EMAIL = "Email"
    DISCORD = "Discord"
    TELEGRAM = "Telegram"

    @classmethod
    def choices(cls) -> dict:
        """Return types as dict."""
        return {member.name: member.value for member in cls}
