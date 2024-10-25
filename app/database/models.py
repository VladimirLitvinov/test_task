from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    code_value = relationship("ReferralCode", backref="author", uselist=False,
                              cascade="all, delete, delete-orphan")


class ReferralCode(Base):
    __tablename__ = 'referralcodes'

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"),
                       nullable=False,
                       unique=True)
    code = Column(String, nullable=False)
    valid_until = Column(Date, nullable=False)

    referrals = relationship("Referral", backref="referralcodes", uselist=True)


class Referral(Base):
    __tablename__ = 'referrals'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"),
                     nullable=False,
                     unique=True)
    code_id = Column(Integer,
                     ForeignKey('referralcodes.id', ondelete="CASCADE"),
                     nullable=False)

    user = relationship("User", backref="referrals", uselist=True)