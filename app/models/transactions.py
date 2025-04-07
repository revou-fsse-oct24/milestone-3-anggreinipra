from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from app.database import db
from sqlalchemy.orm import relationship

# Enum untuk validasi jenis transaksi
class TransactionType(Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"
    transfer = "transfer"

class Transaction(db.Model):
    __tablename__ = "transactions"

    # Mengganti id menjadi transaction_id sebagai primary key
    transaction_id = Column(Integer, primary_key=True, index=True)
    transaction_type = Column(SQLEnum(TransactionType), nullable=False)  # Menggunakan Enum
    amount = Column(Float, nullable=False)
    balance = Column(Float, nullable=False)  # New balance after transaction
    account_number = Column(String(20), ForeignKey('accounts.account_number'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relasi Many-to-One: Transaction (Many) -> Account (One)
    account = relationship("Account", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction {self.transaction_type} - {self.amount} - {self.balance}>"

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "transaction_type": self.transaction_type.value,  # Menyertakan nilai Enum
            "amount": self.amount,
            "balance": self.balance,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
