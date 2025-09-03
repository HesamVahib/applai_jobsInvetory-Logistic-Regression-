import requests
from bs4 import BeautifulSoup
import datetime as dt
import html
from ..category_predictor import categorize_job

url = "https://www.jobly.fi/en/jobs"

def url_updater(page):
    param = {
        'page': page
        }
    data = requests.get(url, params= param)
    data.encoding = 'utf-8'
    soup = BeautifulSoup(data.text, 'html.parser')
    jobs = soup.find_all('div', attrs= {'class': ['mobile_job__content', 'clearfix']})
    return jobs

#print (jobs)
job_dict = {}
yesterday = (dt.date.today() - dt.timedelta(days= 1))

def jobs():

    counter = 0
    page = 0
    not_today = 0

    while True:
        jobs = url_updater(page)

        for job in jobs:
            try:
                try:
                    badge = job.find('span', attrs= {'class' : 'node--job__featured-badge'}).text.strip()
                except:
                    badge = 'not_featured'
                    pass
                # return job_dict
                job_content = job.find('a', attrs= {'class': ['recruiter-job-link', 'recruiter-jobs-new-tab-processed']})
                html_title = job_content['title'].strip()

                title = html.unescape(html_title)
                link = job_content['href']
                locations = job.find('div', attrs= {'class': 'location'}).text.strip().split(', ')
                post_date = job.find('span', attrs = {'class': 'date'}).text.split(',')[0].strip()


                date_as_list = post_date.split('.')
                date_obj = dt.date(int(date_as_list[2]), int(date_as_list[1]), int(date_as_list[0]))
                # print(page)
                if date_obj == yesterday and badge != 'Featured':
                    not_today = 1
                    break

                category = categorize_job(title)

                job_dict[title] = {'link': link, 'locations': locations, 'source': 'jobly', 'category': category}
                counter += 1

                #page += 1
            except:
                continue
        if not_today == 1:
            break
        else:        
            page += 1

    print (f"Jobly is updated by {counter} jobs.")
    return job_dict

if __name__ == "__main__":
    for indx, (i, j) in enumerate(jobs().items()):
        jobs = i
        link = j.get('link')
        locations = ', '.join(j.get('locations', []))
        category = j.get('category')
        print(f"Job {indx + 1}: {i}\nLink: {link}\nLocations: {locations}\nCategory: {category}")
        print('-' * 70)
