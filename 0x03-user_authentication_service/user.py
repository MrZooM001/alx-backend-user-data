#!/usr/bin/env python3
"""Module for authentication service"""

from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """User class"""

    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True)
    email = Column("email", String(250), nullable=False)
    hashed_password = Column("hashed_password", String(250), nullable=False)
    session_id = Column("session_id", String(250), nullable=True)
    reset_token = Column("reset_token", String(250), nullable=True)
