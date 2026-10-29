from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.routers.auth_router import get_current_user
from app.schemas.provider import ProviderCreate, ProviderResponse
from app.services.provider_service import (
    create_provider,
    get_provider_by_user_id,
    ProviderAlreadyExistsError,
)


router = APIRouter(
    prefix="/api/v1/providers",
    tags=["Providers"]
)


@router.post(
    "/me",
    response_model=ProviderResponse,
    status_code=status.HTTP_201_CREATED
)
def register_provider(
    data: ProviderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "CLIENT":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ce compte ne peut pas créer de profil prestataire."
        )

    try:
        return create_provider(db, current_user, data)
    except ProviderAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un profil prestataire existe déjà."
        )


@router.get(
    "/me",
    response_model=ProviderResponse
)
def get_my_provider_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    provider = get_provider_by_user_id(
        db,
        current_user.id
    )

    if provider is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil prestataire introuvable."
        )

    return provider