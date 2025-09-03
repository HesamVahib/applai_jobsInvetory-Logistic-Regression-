from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.firefox.options import Options
import time
import random
from ..category_predictor import categorize_job

# Setup Chrome Driver
chrome_option = Options()
#firefox_option = Options()

chrome_option.add_argument("--headless")
chrome_option.add_argument("--no-sandbox")
chrome_option.add_argument("--log-level=3")
"""firefox_option.add_argument("--headless")
firefox_option.add_argument("--no-sandbox")
firefox_option.add_argument("--log-level=3")"""
driver = webdriver.Chrome(options=chrome_option)

# Setup
location = "Finland"
time_posted = "r86400" # Past 24 hours

# Page Navigator Function
def page_driver(page):
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?location={location}&f_TPR={time_posted}&start={page}"
    driver.get(url)
    time.sleep(random.uniform(1,3))
    final_url = driver.current_url
    while final_url != url: # Skipping Login Page when sudden appears
        driver.get(url)
        final_url = driver.current_url
        time.sleep(random.uniform(1, 5))
    return driver.page_source

job_dict = {}


def jobs():
    counter = 0
    page_counter = 0 # Page Counter to navigate pages

    while True:
        pageSource = page_driver(page_counter)
        if page_counter == 1000 or pageSource == '<html><head></head><body></body></html>': # Once it encounters a Blank Page (no job listed)
            break;
        
        soup = BeautifulSoup(pageSource, 'html.parser')
        jobs = soup.find_all('li') # Jobs are listed in <li> tags

        if jobs:
            for job in jobs:
                try: # What if the error happens on link or posting date ? (Unintended error !!!!)

                    title = job.find('h3', class_='base-search-card__title').text.strip() 

                    link_ref = job.find('a', class_='base-card--link') or job.find('a', class_='base-card__full-link') # Found two Class Names and tryng out both
                    link = link_ref['href']

                    locations = [job.find('span', class_='job-search-card__location').text.strip().split(', ')[0]]

                    # posting_time = job.find('time')['datetime']
                    category = categorize_job(title)

                    job_dict[title] = {'link': link, 'locations': locations, 'source': 'linkedin', 'category': category}
                    counter += 1
                    #print(f'Posted: {posting_time}')
            
                except: # When LinkedIn bans ip

                    page_counter -= 10 # Count Down once it encounters error
                    time.sleep(random.uniform(7,10)) # Simulating human behaviour, haha!

        #print(f"page number : {int(page_counter/10)+1}")
        print(f"page number : {int(page_counter/10)+1}")

        #print('-'*60)
        page_counter += 10
        
        time.sleep(random.uniform(10,15))

    print (f"LinkedIn is updated by {counter} jobs.")
    return job_dict

if __name__ == "__main__":
    for indx, (i, j) in enumerate(jobs().items()):
        jobs = i
        link = j.get('link')
        locations = j.get('locations', [])
        category = j.get('category')
        print(f"Job {indx + 1}: {i}\nLink: {link}\nLocations: {locations}, Category: {category}")
        print('-' * 70)
