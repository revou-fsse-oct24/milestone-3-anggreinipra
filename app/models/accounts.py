from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from app.database import db
from sqlalchemy.orm import relationship

class Account(db.Model):
    __tablename__ = "accounts"
    __table_args__ = (UniqueConstraint('user_id', 'account_number', name='_user_account_uc'),)

    # Menggunakan account_number sebagai primary key
    account_number = Column(String(20), primary_key=True, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)  # Relasi ke user
    balance = Column(Float, default=0.0)
    account_type = Column(String(50), default="basic")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relasi Many-to-One: Account (Many) -> User (One)
    user = relationship("User", back_populates="accounts")
    
    # Relasi One-to-Many ke Transaction
    transactions = relationship('Transaction', back_populates='account')

    def __repr__(self):
        return f"<Account {self.account_number} - {self.user_id}>"

    def to_dict(self):
        return {
            "account_number": self.account_number,
            "balance": self.balance,
            "account_type": self.account_type,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
