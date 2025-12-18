"""
Database models for ExpenseFlow
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    transactions = relationship("Transaction", back_populates="user")
    corrections = relationship("Correction", back_populates="user")


class CategoryEnum(str, enum.Enum):
    """Expense categories"""
    FOOD = "Food"
    TRANSPORT = "Transport"
    BILLS = "Bills"
    SHOPPING = "Shopping"
    ENTERTAINMENT = "Entertainment"
    WORK_SUPPLIES = "Work Supplies"
    HEALTH = "Health"
    OTHER = "Other"


class Transaction(Base):
    """Transaction model"""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    description = Column(String, index=True)
    amount = Column(Float)
    predicted_category = Column(String(50))
    predicted_confidence = Column(Float)
    actual_category = Column(String(50), nullable=True)
    is_corrected = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")
    corrections = relationship("Correction", back_populates="transaction")


class Correction(Base):
    """Feedback/correction model for retraining"""
    __tablename__ = "corrections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), index=True)
    predicted_category = Column(String(50))
    correct_category = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="corrections")
    transaction = relationship("Transaction", back_populates="corrections")
