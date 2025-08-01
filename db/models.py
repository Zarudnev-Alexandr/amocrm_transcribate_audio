from sqlalchemy import DateTime, func, BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class SettingsStrings(Base):
    __tablename__ = "settings_strings"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        index=True,
    )
    gpt_prompt: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    gpt_token: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    whisper_ai_token: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    amo_crm_token: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    amo_crm_link: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
