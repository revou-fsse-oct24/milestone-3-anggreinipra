from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import db

class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    # Menggunakan user_id sebagai primary key
    user_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    user_name = Column(String(100), nullable=False)
    account_number = Column(String(20), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relasi One-to-Many: User (One) -> Account (Many)
    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.user_name} - {self.email}>"

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "email": self.email,
            "account_number": self.account_number,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
