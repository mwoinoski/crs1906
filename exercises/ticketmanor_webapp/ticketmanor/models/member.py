"""
Member model class
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    LargeBinary,
    String,
)
from .person import Person


class Member(Person):
    """Model class for Member
    """
    __tablename__ = 'members'
    id = Column('id', Integer, ForeignKey('people.id'), primary_key=True)
    profile_photo = Column('profilephoto', LargeBinary)
    nick_name = Column('nickname', String)
