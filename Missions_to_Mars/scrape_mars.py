from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "chromedriver.exe"}
    executable_path = {'executable_path': ChromeDriverManager().install()} 
    return Browser("chrome", **executable_path, headless=False)

def scrape_news_title(browser):

    # Scrape data for NASA Mars News
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    # Getting the news title
    results = soup.find_all('div', class_='content_title')

    title = []
    for tag in results:
        # If result element has an anchor...
        if (tag.a):
            # And the anchor has non-blank text...
            if (tag.a.text):
                # Append the text to the list
                title.append(tag.a.text)

    # Return Data
    return(title[0])


def scrape_news_paragraph(browser):

    # Scrape data for NASA Mars News
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Getting the news paragraph
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    # Return Data
    return(news_p)

def scrape_featured_image_url(browser):
    
    ## JPL Mars Space Images - Featured Image
    featured_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    jpl_image_url = 'https://www.jpl.nasa.gov'
    browser.visit(featured_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Getting the featured image
    result = soup.find('article')['style']
    relative_image_path = result.replace('background-image: url(','').replace(');', '').strip()[1:-1]
    featured_image_url = jpl_image_url + relative_image_path
    
    # Return Data
    return(featured_image_url)


def scrape_mars_facts(browser):
    
    fact_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(fact_url)

    fact_df = tables[0]
    fact_df.columns = ['Description','Mars']
    fact_df.set_index('Description', inplace=True)

    html_table = fact_df.to_html(classes = 'table table-striped')

    # Return Data
    return(html_table)


def scrape_mars_hemispheres(browser):

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemisphere_main_url = 'https://astrogeology.usgs.gov'

    browser.visit(hemispheres_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    result_items = soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    for item in result_items:
        # Get the title
        title = item.find('h3').text
        partial_img_url = item.find('a', class_='itemLink product-item')['href']
        complete_url = hemisphere_main_url + partial_img_url
       
        # Visit Url & Create soup object
        browser.visit(complete_url)

        image_html = browser.html
        soup = BeautifulSoup(image_html, 'html.parser')
    
        # Get the title
        image_path = soup.find('img', class_='wide-image')['src']
        img_url = hemisphere_main_url+image_path
    
        hemisphere_image_urls.append({'title':title, 'img_url':img_url})

    # Return Data
    return(hemisphere_image_urls)

def scrape():
    mars_info = {}

    # Initialise browser
    browser = init_browser()

    # Call functions of scraping data
    mars_info['news_title'] = scrape_news_title(browser)
    mars_info['news_p'] = scrape_news_paragraph(browser)
    mars_info['featured_image_url'] = scrape_featured_image_url(browser)
    mars_info['mars_facts'] = scrape_mars_facts(browser)
    mars_info['hemisphere_image_urls'] = scrape_mars_hemispheres(browser)  

    # Close browser
    browser.quit()

    return (mars_info)