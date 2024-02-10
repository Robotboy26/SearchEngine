import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

def get_week_name():
    today = datetime.today()
    month_day = today.strftime("%b_%d")
    return month_day

def scrape_website(url, depth, current_depth):
    if current_depth > depth:
        return
    
    website_name = url.split('//')[1].split('/')[0]
    
    data_dir = 'website_data'
    week_name = get_week_name()
    website_dir = os.path.join(data_dir, week_name, website_name)
    if not os.path.exists(website_dir):
        os.makedirs(website_dir)
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_name = f'{website_name}_{timestamp}.html'
    file_path = os.path.join(website_dir, file_name)
    
    website_response = requests.get(url)
    with open(file_path, 'w') as file:
        file.write(website_response.text)
    
    if current_depth < depth:
        links = extract_urls_from_webpage(url)
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(scrape_website, link, depth, current_depth + 1) for link in links]

def extract_urls_from_webpage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    urls = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('http'):
            urls.append(href)
    
    return urls

def search_and_save(landing_page_url, depth):
    data_dir = 'website_data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    week_name = get_week_name()
    week_dir = os.path.join(data_dir, week_name)
    if not os.path.exists(week_dir):
        os.makedirs(week_dir)
    
    scrape_website(landing_page_url, depth, 0)

landing_page_url = 'https://en.wikipedia.org/wiki/Main_Page'
depth = 2
search_and_save(landing_page_url, depth)
