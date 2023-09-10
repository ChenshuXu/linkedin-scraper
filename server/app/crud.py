from sqlalchemy.orm import Session
from . import models


def get_job_post_view(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.JobPostView).offset(skip).limit(limit).all()


def update_job_post(db: Session, job_post_id: int, status: str):
    job_post = db.query(models.JobPost).filter(models.JobPost.id == job_post_id).first()
    job_post.status = status
    db.commit()
    updated_job_post = db.query(models.JobPostView).filter(models.JobPostView.id == job_post_id).first()
    return updated_job_post


def get_company_all(db: Session):
    return db.query(models.Company).all()


def get_company_by_id(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()
