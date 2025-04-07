from datetime import datetime
from enum import Enum
from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey
from app.database import db
from sqlalchemy.orm import relationship

class TransactionType(Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"
    transfer = "transfer"

class Transaction(db.Model):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    transaction_type = Column(String(20), nullable=False)
    is_transfer = Column(Boolean, default=False)
    transfer_type = Column(String(20), nullable=True)  # transfer_in / transfer_out
    amount = Column(Float, nullable=False)
    balance = Column(Float, nullable=False)
    account_number = Column(String(20), ForeignKey('accounts.account_number'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    account = relationship("Account", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction {self.transaction_type} - {self.amount} - {self.balance}>"

    def to_dict(self):
        return {
            "transaction_id": str(self.transaction_id),
            "transaction_type": self.transaction_type,
            "is_transfer": self.is_transfer,
            "transfer_type": self.transfer_type,
            "amount": self.amount,
            "balance": self.balance,
            "account_number": self.account_number,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
