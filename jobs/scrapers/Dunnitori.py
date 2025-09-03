from matplotlib import category
import requests
from bs4 import BeautifulSoup
import datetime as dt
import html
from ..category_predictor import categorize_job

url = "https://duunitori.fi/tyopaikat"

def url_updater(page):
    param = {
        'sivu': page,
        'order_by': 'date_posted'
    }
    data = requests.get(url, params= param)
    soup = BeautifulSoup(data.text, 'html.parser')
    jobs_place = soup.find('div', attrs= {'class' : 'grid-sandbox--tight-bottom'})
    jobs = jobs_place.find_all('div', attrs= {'class' : 'grid--middle'})
    #scripts = soup.find_all('script')
    return jobs

#c = 0
today_date = dt.date.today()
today_year = today_date.year
yesterday = today_date - dt.timedelta(days= 1)
job_dict = {}

def jobs():
    counter = 0
    page = 0
    title = None
    not_today = 0

    while True:
        c = 0
        if page == 1: page += 1
        jobs = url_updater(page)

        for job in jobs:
            previous_title = title

            try:       
                res = job.find('a', attrs= {'class' : 'gtm-search-result'})
                html_title = job.find('h3', attrs= {'class' : 'job-box__title'}).text
                title = html.unescape(html_title)

                
                if title != previous_title:
                    date_raw = job.find('span', attrs= {'class': 'job-box__job-posted'}).text.split()[1].strip('.')
                    date_list = date_raw.split('.')
                    date_list.append(today_year)
                    date = dt.date(int(date_list[2]), int(date_list[1]), int(date_list[0]))

                    try:
                        locations = [job.find('span', attrs= {'class': 'job-box__job-location'}).text.strip().split(' ')[0]]
                    except:
                        locations = None

                    if date == yesterday:
                        not_today = 1
                        break
                    
                    link = 'https://duunitori.fi' + res['href']

                    category = categorize_job(title)

                    job_dict[title] = {'link': link, 'locations': locations, 'source': 'dunnitori', 'category': category}
                    counter += 1
                    # print(f"job: {title}\nlink: {link}\ndate: {date}\nlocations: {locations}, category: {category}")
                    # c += 1
                    # print(c)
                    # print('-' * 70)
            except:
                pass
        if not_today == 0:
            #print(f"\npage: {page}")
            page += 1
        else:
            break
    
    print(f"Dunnitori is updated by {counter} jobs.")
    return job_dict

if __name__ == "__main__":
    #dict instruction is {title: {link: , locations:[] , source: }}
    for indx, (i, j) in enumerate(jobs().items()):
        jobs = i
        link = j.get('link')
        locations = ', '.join(j.get('locations', []))
        category = j.get('category')
        print(f"Job {indx + 1}: {i}\nLink: {link}\nLocations: {locations}\nCategory: {category}")
        print('-' * 70)
