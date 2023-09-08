from pydantic import BaseModel


class JobPostUpdate(BaseModel):
    id: int
    status: str

    class Config:
        orm_mode = True


class JobPost(JobPostUpdate):
    post_id: str
    url: str
    title: str
    company_id: int
    description: str
    location: str
    timestamp: int
    keywords: str
    search_location: str


class JobPostView(BaseModel):
    id: int
    url: str
    title: str
    description: str
    company_name: str
    location: str
    timestamp: int
    status: str
    keywords: str
    search_location: str

    class Config:
        orm_mode = True


class Company(BaseModel):
    id: int
    company_id: str
    name: str
    url: str

    class Config:
        orm_mode = True
