from typing import Type, Any

from sqlalchemy.orm import Session
from sqlalchemy import select
from database.models import JobPost, Company


# job_post table
def get_job_post(db: Session, job_post_id: str, skip: int = 0, limit: int = 100) -> list[JobPost]:
    return db.query(JobPost).filter(JobPost.post_id == job_post_id).offset(skip).limit(limit).all()


def get_job_post_recent(db: Session, skip: int = 0, limit: int = 100):
    stmt = select(
        JobPost.id,
        JobPost.url,
        JobPost.title,
        JobPost.description,
        Company.name.label('company_name'),
        JobPost.location,
        JobPost.timestamp,
        JobPost.status,
        JobPost.keywords,
        JobPost.search_location,
        JobPost.priority
    ).join(Company).order_by(JobPost.timestamp.desc()).offset(skip).limit(limit)
    res = db.execute(stmt)
    return res


def get_job_post_filtered(db: Session, priority: int, skip: int = 0, limit: int = 100):
    stmt = (select(
        JobPost.id,
        JobPost.url,
        JobPost.title,
        JobPost.description,
        Company.name.label('company_name'),
        JobPost.location,
        JobPost.timestamp,
        JobPost.status,
        JobPost.keywords,
        JobPost.search_location,
        JobPost.priority
    ).join(Company)
    .filter(JobPost.priority > priority)
    .order_by(JobPost.timestamp.desc())
    .offset(skip).limit(limit))
    res = db.execute(stmt)
    return res


def update_job_post(db: Session, id: int, status: str):
    post_to_update = db.query(JobPost).filter(JobPost.id == id).first()
    if post_to_update:
        post_to_update.status = status
        db.commit()

    stmt = select(
        JobPost.id,
        JobPost.url,
        JobPost.title,
        JobPost.description,
        Company.name.label('company_name'),
        JobPost.location,
        JobPost.timestamp,
        JobPost.status,
        JobPost.keywords,
        JobPost.search_location,
        JobPost.priority
    ).join(Company).filter(JobPost.id == id)
    return db.execute(stmt).first()


def add_job_post(db: Session, job_post: JobPost) -> JobPost:
    db.add(job_post)
    db.commit()
    return job_post


# company table
def get_company_all(db: Session) -> list[Type[Company]]:
    return db.query(Company).all()


def add_company(db: Session, company: Company, create_if_not_exit=False) -> Company | None:
    old_company = db.query(Company).filter(
        Company.company_id == company.company_id,
        Company.name == company.name,
        Company.url == company.url
    ).first()
    if old_company:
        return old_company
    if create_if_not_exit:
        db.add(company)
        db.commit()
        return company
    return None
