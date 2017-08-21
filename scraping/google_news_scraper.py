"""
Title:  Google News Search Scraper
Desc:   Extracts search results links, dates & site descriptions from google news search results
Author: Yassin Eltahir
Date:   2017-08-20
"""

from bs4 import BeautifulSoup
import requests
from datetime import datetime
from selenium import webdriver
#import articleDateExtractor


def google_news_url(search_term, start_date, end_date, num_results=100):
    """
    For a given search term and window, build out the corresponding google search term

    :param search_term (str): The word/s you want to search for
    :param start_date (str):  Format = "YYYY-MM-DD"
    :param end_date (str):    Format = "YYYY-MM-DD"
    :param num_results (int): Allowed values are 10, 20, 30, 40, 50, and 100

    :return: URL for your search
    """

    # Prepare the search parameters
    base_url = 'https://www.google.com.au/search?tbm=nws'
    search_field = 'q={}'.format(search_term)
    num_results = 'num={}'.format(num_results)

    # Build the custom date range (dtr)
    min_date = datetime.strptime(start_date,'%Y-%m-%d')
    max_date = datetime.strptime(end_date,'%Y-%m-%d')
    cdr = 'tbs=cdr%3A1%2Ccd_min%3A{}%2F{}%2F{}%2Ccd_max%3A{}%2F{}%2F{}'.format(min_date.month, min_date.day, min_date.year,
                                                                               max_date.month, max_date.day, max_date.year)

    # Build out url
    full_url = [base_url,search_field,cdr,num_results]
    full_url = '&'.join(full_url)

    return full_url



def get_url_metadata(url):
    """
    Attempts to retrieve a sites metadata:
        - Author
        - Description
        - Published Time

    :param url: The web address

    :return: Where possible the author, published date & site description
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'lxml')

    # Get Author
    author_tag = soup.find("meta", property="article:author")
    if not author_tag:
        author_tag = soup.find("meta", attrs={'name': 'author'})

    author = author_tag['content'] if author_tag else None

    # Get Description
    desc_tag = soup.find("meta",  property="og:description")
    desc = desc_tag['content'] if desc_tag else None

    # Get Published Time
    #pub_time = articleDateExtractor.extractArticlePublishedDate(url)
    pub_time = None #until a sub for articleDataExtractor is built.
    pub_time = pub_time.strftime("%Y-%m-%d %H:%M:%S") if pub_time is not None else None


    return author, desc, pub_time




def get_search_results(url, driver_loc):
    """
    Retrieves google search results & gets the page description

    :param url:         Google search url to use
    :param driver_loc:  The location of the chrome webdriver

    :return:
    """

    # Setup & start headless browser
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(executable_path=driver_loc, chrome_options=options)

    # Navigate to the url & extract the results
    browser.get(url)
    xpath_to_find = "//a[@class='l _PMs']"  # Found by using the inspect cmd in chrome.
    results = browser.find_elements_by_xpath(xpath_to_find)

    # For each result, build out the desired data
    search_results = []
    for post in results:

        post_link = post.get_attribute('href')
        post_metadata = {}
        post_metadata['title'] = post.text
        post_metadata['url'] = post_link
        post_metadata['author'], post_metadata['description'], post_metadata['publishedAt'] = get_url_metadata(post_link)

        search_results.append(post_metadata)


    # Close the browsers & return the search results
    browser.quit()
    return search_results




"""
Sample Use:

demo_url = google_news_url('bitcoin', '2017-07-04','2017-07-05', num_results= 10)
driver_location = '<path/to/chrome/driver>'
my_results = get_search_results(demo_url, driver_location)
my_results



"""
