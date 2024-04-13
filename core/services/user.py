from sqlalchemy.orm import Session

from ..models import user as m_user
from ..schemes import user as s_user


def get_user(db: Session, user_id: int):
    return db.query(m_user.User).filter(m_user.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(m_user.User).filter(m_user.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(m_user.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: s_user.UserInDB):
    db_user = m_user.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
