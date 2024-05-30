#!/usr/bin/env python3
"""DB module"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.session import Session
from user import Base, User
import logging

logging.disable(logging.WARNING)

valid_attr = ["id", "email", "hashed_password", "session_id", "reset_token"]


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database"""
        new_user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(new_user)
            self._session.commit()
        except Exception as ex:
            self._session.rollback()
            raise
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find user"""
        session = self.__session
        if not kwargs or any(x not in valid_attr for x in kwargs):
            raise InvalidRequestError()

        try:
            return session.query(User).filter_by(**kwargs).one()
        except Exception as ex:
            raise NoResultFound()

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user"""
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise NoResultFound()

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError()

            setattr(user, key, value)
        try:
            self.__session.commit()
        except InvalidRequestError:
            raise ValueError()
