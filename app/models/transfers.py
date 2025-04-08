from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import db


# Model untuk transfer antar akun
class Transfer(db.Model):
    __tablename__ = "transfers"

    transfer_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    from_account = Column(String(20), ForeignKey("accounts.account_number"), nullable=False)
    to_account = Column(String(20), ForeignKey("accounts.account_number"), nullable=False)
    amount = Column(Float, nullable=False)
    balance = Column(Float, nullable=False)  # balance setelah transfer dilakukan
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relasi ke akun pengirim dan penerima
    from_account_rel = relationship("Account", foreign_keys=[from_account], back_populates="transfers_out")
    to_account_rel = relationship("Account", foreign_keys=[to_account], back_populates="transfers_in")

    def __repr__(self):
        return f"<Transfer {self.from_account} -> {self.to_account} | {self.amount}>"

    def to_dict(self):
        return {
            "transfer_id": self.transfer_id,
            "from_account": self.from_account,
            "to_account": self.to_account,
            "amount": self.amount,
            "balance": self.balance,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
