from sqlalchemy import Integer,Column,String,DateTime,ForeignKey,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import func
from models.database import engine,Base
import uuid

class User(Base):
    __tablename__= "user"
    id = Column(Integer(), primary_key=True)
    email = Column(String(200), unique=True)
    username = Column(String(100),unique=True)
    password =Column(String(20))
    urls= relationship('URL',back_populates = "url_owner")
    user_profile = relationship('Profile',back_populates = "user")
    profile_image = relationship('ProfileImage',back_populates = "owner")
    
    def __repr__(self):
        return f"User {self.username}"
 
class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer(), primary_key=True)
    firstname = Column(String(100),nullable=False)
    lastname = Column(String(100),nullable=False)
    bio = Column(String(500),nullable=False)
    gender = Column(String(100),nullable=False)
    created_at =Column(DateTime(timezone=True), server_default = func.now())
    user = relationship('User',back_populates = "user_profile")
    user_id = Column(Integer(), ForeignKey('user.id'))

class ProfileImage(Base):
    __tablename__= "profileimages"
    id = Column(Integer(), primary_key=True)
    name = Column(String(200))
    img = Column(String(100))
    minetype = Column(String(100))
    user_id = Column(Integer(), ForeignKey('user.id'))
    owner = relationship('User',back_populates = "profile_image")

class URL(Base):
    __tablename__= "urls"
    id = Column(Integer(), primary_key=True)
    original_url = Column(String(500))
    short_url = Column(String(200))
    url_key = Column(String(200))
    custom_url = Column(String(200))
    custom_domain = Column(String(200))
    clicks = Column(Integer(),default=0)
    is_active = Column(Boolean(),default=True)
    timestamp = Column(DateTime(timezone=True), server_default = func.now())
    user_id = Column(Integer(), ForeignKey('user.id'))
    url_owner = relationship('User',back_populates="urls")
    qr_image = relationship('QR',back_populates="url_details")

    def __repr__(self):
        return f"URL {self.original_url} and by Short:{self.short_url}"

class QR(Base):
    __tablename__="qrcodes"
    id = Column(Integer(), primary_key=True)
    image = Column(String(500))
    url_id = Column(Integer(),ForeignKey('urls.id'))
    url_details = relationship("URL",back_populates="qr_image")
    
    def __repr__(self):
        return f"URL QRcode : {self.url_id}"

Base.metadata.create_all(bind=engine)