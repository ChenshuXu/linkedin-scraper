import json
from linkedin_api import Linkedin

USERNAME = "chenshux@usc.edu"
PASSWORD = "jaywalker-diary-dried"

linkedin = Linkedin(USERNAME, PASSWORD, debug=True)

jobDetail = linkedin.get_job("3666325857")
with open("jobDetail_3666325857.json", "w") as f:
    json.dump(jobDetail, f, indent=4)