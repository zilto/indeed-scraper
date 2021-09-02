import requests
from bs4 import BeautifulSoup

from job_model import JobType


BASE_URL = "https://ca.indeed.com/"

all_entries = []

def _get_entries(soup):
    def _get_title(job):
        return job.find("h2", class_="title").a.text.strip()

    def _get_company(job):
        if job.find("span", class_="company") is not None:
            return job.find("span", class_="company").text.strip()
        else:
            return None

    def _get_salary(job):
        if job.find("span", class_="salaryText") is not None:
            return job.find("span", class_="salaryText").text.strip()
        else:
            return None

    def _get_description(job):
        # <div id="jobDescriptionText" class="jobsearch-jobDescriptionText">
        pass

    def _get_link(job):
        base_url = "https://ca.indeed.com/viewjob?jk="
        return base_url + job["data-jk"]

    page_entries = []
    job_list = soup.find_all("div", class_="jobsearch-SerpJobCard")
    for job in job_list:
        entry = JobType(title=_get_title(job),
                        company = _get_company(job),
                        salary = _get_salary(job),
                        description = None,
                        link = _get_link(job))
        page_entries.append(entry)
    return page_entries


def get_all_pages(url="https://ca.indeed.com/jobs", job_name=None, location=None):
    query = {"q": job_name, "l": location}
    r = requests.get(url, params=query, timeout=5)

    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, "lxml")

        global all_entries
        all_entries.extend(_get_entries(soup))

        last_button = soup.find("ul", class_="pagination-list").find_all("li")[-1]
        if last_button.a is not None:
            if last_button.a["aria-label"] == "Next":
                new_url = BASE_URL + last_button.a["href"]
                get_all_pages(new_url)

        return all_entries
