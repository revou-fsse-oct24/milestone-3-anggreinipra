from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import db

class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True} 
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(10), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    user_name = Column(String(100), nullable=False)
    account_number = Column(String(20), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.user_name} - {self.email}>"
