from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as PgEnum
from sqlalchemy.orm import relationship
from app.database import db


# Enum untuk jenis transaksi (deposit, withdrawal)
class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


# Model transaksi untuk deposit dan withdrawal
class Transaction(db.Model):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    transaction_type = Column(PgEnum(TransactionType, name="transaction_type_enum", create_type=True), nullable=False)
    amount = Column(Float, nullable=False)
    balance = Column(Float, nullable=False)
    account_number = Column(String(20), ForeignKey("accounts.account_number"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relasi ke model Account
    account = relationship("Account", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction {self.transaction_type.value} - {self.amount}>"

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "transaction_type": self.transaction_type.value,
            "amount": self.amount,
            "balance": self.balance,
            "account_number": self.account_number,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
