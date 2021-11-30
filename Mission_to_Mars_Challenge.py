
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site
# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[11]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[14]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[15]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

#parse the resulting html with soup
html = browser.html
hemi_soup = soup(html, 'html.parser')

# title_results = hemi_soup.find_all('div', class_="item")
# image_url_results = hemi_soup.find_all('div', class_="item")

results = hemi_soup.find_all('div', class_="item")
results2 = hemi_soup.find('img', class_="thumb").get('src')

# print(results)
# print(results2)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

# get the titles
for result in results:
    hemisphere = {}
#     image_elem = browser.find_by_("a['href'])[1]
#     image_elem.click()
    title = result.find("h3").text
    
    image_url = result.find('img')['src']
#     print(image_url)
    
    #get the urls
#     image_url = result.a['href']
    actual_image_url = url + image_url
    
#     for link in hemi_soup.find_all('img'):
#         print(link.get('src'))
    
    hemisphere_image_urls.append({"image url": image_url, "title": title})

#     browser.back()

# #     print(image_url)
    print(actual_image_url)
#     print(title)

# 4. Print the list that holds the dictionary of each image url and title.

print(hemisphere_image_urls)

# 5. Quit the browser
browser.quit()

