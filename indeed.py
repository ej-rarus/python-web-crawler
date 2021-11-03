import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=Python&limit={LIMIT}&sort=date"

def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})

    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    max_page = pages[-1]
    return max_page

def extract_job(html):
    job_dict = {}
    if html.find("span", {"class": "companyName"}) is not None:
        title = html.find("h2", {"class": "jobTitle"}).text.strip("new")
        company = html.find("span", {"class": "companyName"}).string
        location = html.find("div", {"class": "companyLocation"}).string
        job_id = html['data-jk']
        job_dict = {"title":title,
                    "company":company,
                    "location":location,
                    "link": f"https://kr.indeed.com/viewjob?jk={job_id}&tk=1fjfu7868smmh801&from=serp&vjs=3"
                    }
    else: pass
    return job_dict

def getting_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Page {page+1}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("a", {"class": "tapItem"})
        for result in results[:-1]:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    last_page = get_last_page()
    jobs = getting_jobs(20)
    return jobs