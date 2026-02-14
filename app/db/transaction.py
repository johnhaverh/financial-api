from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class TransactionDB(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    type_ = Column(String)
    amount = Column(Float)
    currency = Column(String)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    account_id = Column(String, ForeignKey("accounts.account_id"))
    account = relationship("AccountDB", back_populates="transactions")
