from linkedin_api import Linkedin
from database import crud, models
from database.database import SessionLocal, engine
import logging
import json

logger = logging.getLogger(__name__)

filter_company_id = [1, 45, 90]
filter_words = ["senior", "site reliability", "sr.", "staff", "principle", "dev ops"]
important_words = ["junior", "jr", "jr.", "entry level", "associate"]


def get_priority_of_job_post(job_post: models.JobPost, company: models.Company) -> int:
    if company.id in filter_company_id:
        return 0

    title = job_post.title.lower()
    for w in important_words:
        if w in title:
            return 1
    for w in filter_words:
        if w in title:
            return 0
    return 10


class LinkedinScraper:
    def __init__(self, username, password, debug=False):
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
        self.logger = logger
        self.db = SessionLocal()
        self.linkedin = Linkedin(username, password, debug=debug)

    def insert_job_post(self, job_detail: dict):
        if job_detail["status"] == "fail":
            return

        company_details = job_detail["company_details"]
        company = models.Company(company_id=company_details["company_id"],
                                 name=company_details["name"],
                                 url=company_details["url"])
        company = crud.add_company(self.db, company, create_if_not_exit=True)

        job_post = models.JobPost(post_id=job_detail["post_id"],
                                  url=job_detail["url"],
                                  title=job_detail["title"],
                                  company_id=company.id,
                                  description=job_detail["description"],
                                  location=job_detail["location"],
                                  timestamp=job_detail["timestamp"],
                                  status=job_detail["status"],
                                  keywords=job_detail["keywords"],
                                  search_location=job_detail["search_location"])
        priority = get_priority_of_job_post(job_post, company)
        job_post.priority = priority
        post = crud.add_job_post(self.db, job_post)
        self.logger.debug("new post added, {}".format(post))

    def search_jobs(self, keywords: str = "software engineer", location_name: str = "United States",
                    distance: int = None, listed_at: int = 24 * 60 * 60, limit: int = 20):
        jobs = self.linkedin.search_jobs(keywords=keywords, location_name=location_name, distance=distance,
                                         listed_at=listed_at, limit=limit)
        self.logger.info("get {} jobs".format(len(jobs)))

        for job in jobs:
            post_id = job['entityUrn'].split(':')[-1]  # "trackingUrn": "urn:li:jobPosting:3648431448"
            # check if post exist
            if crud.get_job_post(self.db, post_id):
                self.logger.debug("post id {} exist".format(post_id))
                continue

            job_post_detail = {
                "post_id": post_id,
                "keywords": keywords,
                "search_location": location_name,
                "status": "fail"
            }
            try:
                job_detail_data = self.linkedin.get_job(post_id)

                company_details = job_detail_data["companyDetails"][
                    "com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany"]["companyResolutionResult"]

                job_post_detail.update({
                    "status": "success",
                    "url": "https://www.linkedin.com/jobs/view/{}/".format(post_id),
                    "company_details": {
                        "company_id": company_details["entityUrn"],
                        "name": company_details["name"],
                        "url": company_details["url"]
                    },
                    "location": job_detail_data["formattedLocation"],
                    "description": job_detail_data["description"]["text"],
                    "title": job_detail_data["title"],
                    "timestamp": int(job_detail_data["listedAt"] / 1000)
                })
            except Exception as e:
                self.logger.error("fail when get job detail id: {}, error: {}".format(post_id, e))
            finally:
                self.logger.debug("{} get job detail id: {}".format(job_post_detail["status"], post_id))
                self.insert_job_post(job_post_detail)


if __name__ == "__main__":
    with open("credentials.json", "r") as f:
        credentials = json.load(f)

    scraper = LinkedinScraper(credentials["username"], credentials["password"], debug=True)
    scraper.search_jobs(listed_at=24 * 60 * 60, limit=200)
    scraper.search_jobs(location_name="seattle", listed_at=24 * 60 * 60, limit=200)
