from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from . import schemas
from database import models, crud
from database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/job_post_update/", response_model=schemas.JobPostView)
def update_job_post(job_post: schemas.JobPostUpdate, db: Session = Depends(get_db)):
    return crud.update_job_post(db, job_post.id, job_post.status)


@app.get("/job_post_all/", response_model=list[schemas.JobPostView])
def read_job_post_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    job_posts = crud.get_job_post_recent(db, skip=skip, limit=limit)
    return job_posts


@app.get("/job_post_filtered/", response_model=list[schemas.JobPostView])
def read_job_post_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    job_posts = crud.get_job_post_filtered(db, 0, skip=skip, limit=limit)
    return job_posts

