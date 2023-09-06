from linkedin_api import Linkedin
import datetime
import pytz
import sqlite3
import logging
import json

logger = logging.getLogger(__name__)


class LinkedinScraper:
    def __init__(self, username, password, debug=False):
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
        self.logger = logger
        self.linkedin = Linkedin(username, password, debug=debug)
        self._connect_db()

    def _connect_db(self):
        self.connection = sqlite3.connect('jobPostDB.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            '''
            create table if not exists company
            (
                id          INTEGER
                    constraint company_pk
                        primary key autoincrement,
                companyId   TEXT not null,
                companyName TEXT,
                companyUrl  TEXT,
                constraint company_pk2
                    unique (companyId, id)
            );
            '''
        )
        self.connection.commit()

        self.cursor.execute(
            '''
            create table if not exists jobPost
            (
                id            INTEGER
                    constraint jobPost_pk
                        primary key autoincrement,
                jobId         TEXT not null,
                jobUrl        TEXT,
                title         TEXT,
                companyId     INTEGER
                    constraint jobPost_companyId_fk
                        references company,
                description   TEXT,
                location      TEXT,
                postTime      TEXT,
                postTimeStamp INTEGER,
                status        TEXT,
                constraint jobPost_pk2
                    unique (jobId, id)
            );
            '''
        )
        self.connection.commit()

        self.cursor.execute(
            '''
            create table if not exists log
            (
                id        INTEGER
                    constraint log_pk
                        primary key autoincrement,
                timeStamp INTEGER,
                jobPostId INTEGER not null
                    constraint log_pk2
                        unique
                    constraint log_jobPost_id_fk
                        references jobPost,
                message   TEXT
            );
            '''
        )
        self.connection.commit()

    def _get_company_id(self, company_id: str, company_name: str, company_url: str) -> int:
        self.cursor.execute("SELECT id FROM company WHERE companyId = ? AND companyName = ? AND companyUrl = ?;",
                            (company_id, company_name, company_url))
        row = self.cursor.fetchone()
        if row is None:
            self.cursor.execute("INSERT INTO company (companyId, companyName, companyUrl) VALUES (?, ?, ?);",
                                (company_id, company_name, company_url))
            self.connection.commit()
            company_row_id = self.cursor.lastrowid
        else:
            company_row_id = int(row[0])

        return company_row_id

    def _get_job_post(self, job_id: str) -> list:
        self.cursor.execute("SELECT * FROM jobPost WHERE jobId = ?", (job_id,))
        return self.cursor.fetchall()

    def _insert_job_post(self, job_detail):
        if job_detail["status"] == "fail":
            return

        company_details = job_detail["companyDetails"]
        company_id = self._get_company_id(company_details["companyId"],
                                          company_details["companyName"],
                                          company_details["companyUrl"])
        # check if post exist
        self.cursor.execute("SELECT * FROM jobPost WHERE jobId = ?", (job_detail["jobId"],))
        rows = self.cursor.fetchall()
        if not rows:
            self._insert_job_post_row(job_detail, company_id)

    def _insert_job_post_row(self, job_detail, company_id) -> int:
        sql = '''
            insert into jobPost (jobId, jobUrl, title, companyId, description, location, postTime, postTimeStamp, status) 
            values (?,?,?,?,?,?,?,?,?);
        '''
        self.cursor.execute(sql, [
            job_detail["jobId"],
            job_detail["jobUrl"],
            job_detail["title"],
            company_id,
            job_detail["description"],
            job_detail["location"],
            job_detail["postTime"],
            job_detail["postTimeStamp"],
            job_detail["status"]
        ]
                            )
        self.connection.commit()
        return self.cursor.lastrowid

    def _insert_log(self, job_id: int, message: str):
        sql = '''
        insert into main.log ("timeStamp", jobPostId, message)
        values (?,?,?);
        '''
        self.cursor.execute(sql, (int(datetime.datetime.now().timestamp()), job_id, message))
        self.connection.commit()

    def search_jobs(self, keywords: str = "software engineer", location_name: str = "United States",
                    distance: int = None, listed_at: int = 24 * 60 * 60, limit: int = 20):
        jobs = self.linkedin.search_jobs(keywords=keywords, location_name=location_name, distance=distance,
                                         listed_at=listed_at, limit=limit)
        self.logger.info("get {} jobs".format(len(jobs)))
        job_details = []

        for job in jobs:
            job_id = job['entityUrn'].split(':')[-1]  # "trackingUrn": "urn:li:jobPosting:3648431448"
            # check if post exist
            if self._get_job_post(job_id):
                self.logger.debug("job id {} exist".format(job_id))
                continue

            job_detail = {
                "jobId": job_id,
                "status": "fail"
            }
            try:
                job_detail_data = self.linkedin.get_job(job_id)

                company_details = job_detail_data["companyDetails"][
                    "com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany"]["companyResolutionResult"]

                job_url = "https://www.linkedin.com/jobs/view/{}/".format(job_id)

                listed_time = datetime.datetime.fromtimestamp(job_detail_data["listedAt"] / 1000)
                pdt_tz = pytz.timezone('America/Los_Angeles')
                pdt_dt = pdt_tz.localize(listed_time)
                pdt_str = pdt_dt.strftime('%Y-%m-%d %H:%M:%S %Z')

                job_detail.update({
                    "status": "success",
                    "jobUrl": job_url,
                    "companyDetails": {
                        "companyId": company_details["entityUrn"],
                        "companyName": company_details["name"],
                        "companyUrl": company_details["url"]
                    },
                    "location": job_detail_data["formattedLocation"],
                    "description": job_detail_data["description"]["text"],
                    "title": job_detail_data["title"],
                    "postTime": pdt_str,
                    "postTimeStamp": listed_time.timestamp()
                })
            except Exception as e:
                self.logger.error("fail when get job detail id: {}, error: {}".format(job_id, e))
                self._insert_log(job_id, str(e))
            finally:
                self.logger.debug("{} get job detail id: {}".format(job_detail["status"], job_id))
                self._insert_job_post(job_detail)
                job_details.append(job_detail)
        return job_details


with open("credentials.json", "r") as f:
    credentials = json.load(f)

scraper = LinkedinScraper(credentials["username"], credentials["password"], debug=True)
scraper.search_jobs(limit=200)
