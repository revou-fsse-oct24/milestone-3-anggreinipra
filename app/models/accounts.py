from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import db


class Account(db.Model):
    __tablename__ = "accounts"
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String(20), unique=True, nullable=False)  # Format: DDMMYY-XXXXXX
    account_type = Column(String(50), nullable=False)  # e.g., 'savings', 'checking'
    balance = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # FOREIGN KEY to users.id
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # RELATIONSHIP: Many-to-One (Account ➝ User)
    user = relationship("User", back_populates="accounts")

    # RELATIONSHIP: One-to-Many (Account ➝ Transactions)
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Account {self.account_number} | Balance: {self.balance}>"
