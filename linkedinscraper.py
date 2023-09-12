from linkedin_api import Linkedin
import datetime
import sqlite3
import logging
import json

logger = logging.getLogger(__name__)


class LinkedinScraper:
    def __init__(self, username, password, debug=False):
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
        self.logger = logger
        self._connect_db()
        self.linkedin = Linkedin(username, password, debug=debug)

    def _connect_db(self):
        self.connection = sqlite3.connect('linkedin_job_post_DB.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            '''
            create table if not exists company
            (
                id          INTEGER
                    constraint company_pk
                        primary key autoincrement,
                company_id   TEXT not null,
                name TEXT,
                url  TEXT
            );
            '''
        )
        self.connection.commit()

        self.cursor.execute(
            '''
            create table if not exists job_post
            (
                id              INTEGER
                    constraint job_post_pk
                        primary key autoincrement,
                post_id         TEXT not null,
                url             TEXT,
                title           TEXT,
                company_id      INTEGER
                    constraint job_post_company_id_fk
                        references company,
                description     TEXT,
                location        TEXT,
                timestamp       INTEGER,
                status          TEXT,
                keywords        TEXT,
                search_location TEXT
            );
            '''
        )
        self.connection.commit()

        self.cursor.execute(
            '''
            create table if not exists logger
        (
            id        INTEGER
                constraint log_pk
                    primary key autoincrement,
            timestamp INTEGER,
            post_id   INTEGER not null
                constraint logger_job_post_id_fk
                    references job_post,
            message   TEXT
        );
            '''
        )
        self.connection.commit()

        self.cursor.execute('''
        CREATE VIEW if not exists job_post_view as
        select job_post.id, job_post.url, title, description, c.name as company_name, location, timestamp, status, keywords, search_location from job_post 
        left join company c on c.id = job_post.company_id order by timestamp desc;
        ''')
        self.connection.commit()

    def _get_company_id(self, company_id: str, name: str, url: str) -> int:
        self.cursor.execute("SELECT id FROM company WHERE company_id = ? AND name = ? AND url = ?;",
                            (company_id, name, url))
        row = self.cursor.fetchone()
        if row is None:
            self.cursor.execute("INSERT INTO company (company_id, name, url) VALUES (?, ?, ?);",
                                (company_id, name, url))
            self.connection.commit()
            company_row_id = self.cursor.lastrowid
        else:
            company_row_id = int(row[0])

        return company_row_id

    def _get_job_post(self, job_id: str) -> list:
        self.cursor.execute("SELECT * FROM job_post WHERE post_id = ?", (job_id,))
        return self.cursor.fetchall()

    def _insert_job_post(self, job_detail):
        if job_detail["status"] == "fail":
            return

        company_details = job_detail["company_details"]
        company_id = self._get_company_id(company_details["company_id"],
                                          company_details["name"],
                                          company_details["url"])
        # check if post exist
        self.cursor.execute("SELECT * FROM job_post WHERE post_id = ?", (job_detail["post_id"],))
        rows = self.cursor.fetchone()
        if not rows:
            self._insert_job_post_row(job_detail, company_id)

    def _insert_job_post_row(self, job_detail, company_id) -> int:
        sql = '''
            insert into job_post (post_id, url, title, company_id, description, location, timestamp, status, keywords, search_location) 
            values (?,?,?,?,?,?,?,?,?,?);
        '''
        self.cursor.execute(sql, [
            job_detail["post_id"],
            job_detail["url"],
            job_detail["title"],
            company_id,
            job_detail["description"],
            job_detail["location"],
            job_detail["timestamp"],
            job_detail["status"],
            job_detail["keywords"],
            job_detail["search_location"]
        ]
                            )
        self.connection.commit()
        return self.cursor.lastrowid

    def _insert_log(self, job_id: int, message: str):
        sql = '''
        insert into logger ("timestamp", post_id, message)
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
            post_id = job['entityUrn'].split(':')[-1]  # "trackingUrn": "urn:li:jobPosting:3648431448"
            # check if post exist
            if self._get_job_post(post_id):
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
                self._insert_log(post_id, str(e))
            finally:
                self.logger.debug("{} get job detail id: {}".format(job_post_detail["status"], post_id))
                self._insert_job_post(job_post_detail)
                job_details.append(job_post_detail)
        return job_details


with open("credentials.json", "r") as f:
    credentials = json.load(f)

scraper = LinkedinScraper(credentials["username"], credentials["password"], debug=True)
scraper.search_jobs(listed_at=24 * 60 * 60, limit=400)
scraper.search_jobs(location_name="seattle", listed_at=24 * 60 * 60, limit=400)
