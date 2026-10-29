from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import UserRegister
from app.core.security import hash_password, verify_password


class EmailAlreadyExistsError(Exception):
    pass


def get_user_by_email(db: Session, email: str) -> User | None:
    normalized_email = email.strip().lower()

    statement = select(User).where(User.email == normalized_email)

    return db.scalar(statement)


def create_user(db: Session, user_data: UserRegister) -> User:
    email = str(user_data.email).strip().lower()

    existing_user = get_user_by_email(db, email)

    if existing_user is not None:
        raise EmailAlreadyExistsError("Cet email est déjà utilisé.")

    user = User(
        email=email,
        password_hash=hash_password(user_data.password),
        role="CLIENT",
        is_active=True,
        is_verified=False
    )

    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise EmailAlreadyExistsError(
            "Cet email est déjà utilisé."
        )

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str
) -> User | None:

    user = get_user_by_email(db, email)

    if user is None:
        return None

    if not verify_password(password, user.password_hash):
        return None

    if not user.is_active:
        return None

    return user