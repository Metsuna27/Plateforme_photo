from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProviderCreate(BaseModel):
    business_name: str = Field(min_length=2, max_length=255)
    siret: str | None = Field(
        default=None,
        pattern=r"^\d{14}$"
    )


class ProviderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    business_name: str
    siret: str | None
    created_at: datetime