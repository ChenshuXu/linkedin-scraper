from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from .database import Base


class JobPost(Base):
    __tablename__ = "job_Post"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(String)
    url = Column(String)
    title = Column(String)
    company_id = Column(Integer, ForeignKey("company.id"))
    description = Column(String)
    location = Column(String)
    timestamp = Column(Integer)
    status = Column(String)
    keywords = Column(String)
    search_location = Column(String)


class JobPostView(Base):
    __tablename__ = "job_post_view"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    title = Column(String)
    description = Column(String)
    company_name = Column(String)
    location = Column(String)
    timestamp = Column(Integer)
    status = Column(String)
    keywords = Column(String)
    search_location = Column(String)


class Company(Base):
    __tablename__ = "company"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(String)
    name = Column(String)
    url = Column(String)
