from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.provider import Provider
from app.models.user import User
from app.schemas.provider import ProviderCreate


class ProviderAlreadyExistsError(Exception):
    pass


def get_provider_by_user_id(
    db: Session,
    user_id
) -> Provider | None:
    statement = select(Provider).where(
        Provider.user_id == user_id
    )

    return db.scalar(statement)


def create_provider(
    db: Session,
    user: User,
    data: ProviderCreate
) -> Provider:

    existing_provider = get_provider_by_user_id(
        db,
        user.id
    )

    if existing_provider is not None:
        raise ProviderAlreadyExistsError()

    provider = Provider(
        user_id=user.id,
        business_name=data.business_name.strip(),
        siret=data.siret
    )

    db.add(provider)
    user.role = "PROVIDER"

    try:
        db.commit()
        db.refresh(provider)
    except IntegrityError:
        db.rollback()
        raise ProviderAlreadyExistsError()

    return provider