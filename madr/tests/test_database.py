from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database.models import User


def test_create_user(session: Session):
    user = User(
        username='fausto', email='fausto@fausto.com', password='[HASH_PWD]'
    )
    session.add(user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'fausto'))

    assert user.username == 'fausto'
