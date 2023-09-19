from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class JobPost(Base):
    __tablename__ = "job_post"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(String, index=True)
    url = Column(String)
    title = Column(String)
    company_id = Column(Integer, ForeignKey("company.id"))
    description = Column(String)
    location = Column(String)
    timestamp = Column(Integer)
    status = Column(String)
    keywords = Column(String)
    search_location = Column(String)
    priority = Column(Integer)
    description_keywords = Column(String)

    def __repr__(self) -> str:
        return f"JobPost(id={self.id}, post_id={self.post_id}, title={self.title})"


class Company(Base):
    __tablename__ = "company"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(String, index=True)
    name = Column(String)
    url = Column(String)

    def __repr__(self) -> str:
        return f"Company(id={self.id}, post_id={self.company_id}, title={self.name})"
