#import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# set your executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def mars_news():
#, then set up the URL for scraping
#visit the mars nasa news site
    url = 'http:redplanetscience.com/'
    browser.visit(url)

#optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

#ABOVE CODE
#code accomplishes 2 things:
# 1. we're searching for elements with a specific combination of tag (div) and attribute (list_text).
# 2. we're also telling our browser to wait one second before searching for components. 
# the optional delay is useful because sometimes dynamic pages take a little while to load, especially if theya re image-heavy

#set up the html parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')

# Notice how we've assigned slide_elem as the variable to look for the <div /> tag and its descendent (the other tags within
# the <div /> element)? This is our parent element. This means that this element holds all of the other elements within it, 
# and we'll reference it when we want to filter search results even further. The . is used for selecting classes, such as 
# list_text, so the code 'div.list_text' pinpoints the <div /> tag with the class of list_text. CSS works from right to left,
# such as returning the last item on the list instead of the first. Because of this, when using select_one, the first 
# matching element returned will be a <li /> element with a class of slide and all nested elements within it.

#Robin wants to collect the most recent news artcile along with its summary

#assign the title and summary text to variables we'll reference later
    slide_elem.find('div', class_='content_title')

# use the parent element to find the first 'a' tag and save it as 'news_title' 
    news_title = slide_elem.find('div', class_='content_title').get_text()
    news_title

# use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    news_p

# ### Image Scraping

#visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# find the click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

#parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

#find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

#CODE ABOVE
# an img tag is nested within this HTML, so we've included it.
# .get('src') pulls the link to the image

#what we've done here is tell BeautifulSoup to look inside the <img /> tag for an image with a class of fancybox-image
# Basically we're saying, "this is where the image we want lives - use the link that's inside these tags"

#use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

#scrape the entire table with Pandas

# creating a DataFrame from the HTML table.
# the Pandas function read_html() specifically searches for and returns a list of tables found in the HTMl.
#by specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or teh first item in the list.
df = pd.read_html('https://galaxyfacts-mars.com')[0]

#we assign columns to the new DataFrame for additional clarity
df.columns=['description', 'Mars', 'Earth']

#by using .set_index() function, we're turning the description column into the DataFrame's index.
#inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.
df.set_index('description', inplace=True)
df

#convert our DF back into HTML-ready code using the .to_html() function.
df.to_html()

#end the automated browsing session.
browser.quit()

