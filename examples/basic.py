from linkedin_api import Linkedin

USERNAME = "chenshux@usc.edu"
PASSWORD = "jaywalker-diary-dried"
PUBLIC_PROFILE_ID = "chenshu-xu"
PROFILE_ID = "ACoAABdMtAUB1ORayXH2URJzEym1lJ8_M34crTA"

linkedin = Linkedin(USERNAME, PASSWORD, debug=True)

jobs = linkedin.search_jobs(keywords="software engineer", limit=5)
print(jobs)
