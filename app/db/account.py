from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from .database import Base


class AccountDB(Base):
    __tablename__ = "accounts"

    account_id = Column(String, primary_key=True, index=True)
    balance = Column(Float, default=0)

    transactions = relationship(
        "TransactionDB",
        back_populates="account",
        cascade="all, delete"
    )
