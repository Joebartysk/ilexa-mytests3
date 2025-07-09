# app/models/Users.py
from sqlalchemy import Column, Integer, String, TEXT, ForeignKey, Date, UniqueConstraint, Index, \
	Enum as SQLAlchemyEnum, Boolean, TIMESTAMP as SQLAlchemyTimestamp
from sqlalchemy.ext.declarative import declarative_base
import sys
import os
from datetime import datetime
import pytz
import uuid

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Base = declarative_base()

# Definimos el tipo de usuario para la columna status
UserStatus = SQLAlchemyEnum('pending_verification', 'active', 'inactive', name='user_status')

class User(Base):
	__tablename__ = "users"
	__table_args__ = (
		UniqueConstraint('verification_token'),
		UniqueConstraint('reset_password_token'),
		Index('idx_users_email', 'email'),
		{"schema": "licensing"}
	)

	id = Column(Integer, primary_key=True, autoincrement=True)

	email = Column(String(255), nullable=False, unique=True)
	password_hash = Column(String(255), nullable=False)

	first_name = Column(String(100), nullable=False)
	last_name = Column(String(100), nullable=False)

	phone = Column(String(20))

	status = Column(UserStatus, default='pending_verification', nullable=False)
	email_verified = Column(Boolean, default=False, nullable=True)

	created_at = Column(SQLAlchemyTimestamp, default=datetime.now(pytz.utc), nullable=False)
	updated_at = Column(SQLAlchemyTimestamp, default=datetime.now(pytz.utc), onupdate=datetime.now(pytz.utc), nullable=False)
	last_login = Column(SQLAlchemyTimestamp)

	verification_token = Column(String(36))
	verification_token_expire_at = Column(SQLAlchemyTimestamp, default=datetime.now(pytz.utc), nullable=False)  # Almacenar UUID como cadena
	reset_password_token = Column(String(36))
	reset_token_expires_at = Column(SQLAlchemyTimestamp)

	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		if kwargs.get("verification_token") is None:
			self.verification_token = str(uuid.uuid4())
		if kwargs.get("reset_password_token") is None:
			self.reset_password_token = str(uuid.uuid4())

	@property
	def full_name(self):
		return f"{self.first_name} {self.last_name}"

	def set_reset_password_token(self):
		self.reset_password_token = str(uuid.uuid4())
