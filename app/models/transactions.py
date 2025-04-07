from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import db

class Transaction(db.Model):
    __tablename__ = "transactions"
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, index=True)
    transaction_type = Column(String(20), nullable=False)  # deposit, withdrawal, transfer
    amount = Column(Float, nullable=False)
    balance = Column(Float, nullable=False)  # balance after transaction
    date_transaction = Column(DateTime, default=datetime.utcnow)
    description = Column(String(255), nullable=True)

    # Foreign Key ke Account
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)

    # Relasi Many-to-One: Transaction (Many) -> Account (One)
    account = relationship("Account", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction {self.transaction_type} - {self.amount} - {self.date_transaction}>"
