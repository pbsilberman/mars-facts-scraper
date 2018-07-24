

```python
# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
```

## NASA Mars News


```python
# Use splinter to start up a Chrome driver
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
```


```python
# Send the browser to NASA's news page
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
browser.visit(url)
```


```python
# HTML object
html = browser.html

# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')
```


```python
# Pull the list of articles
article_list = soup.find('ul', class_='item_list')

# Extract the most recent article's title
news_title = article_list.h3.text

# Extract the most recent article's description
news_p = article_list.find('div', class_="rollover_description_inner").text
```


```python
print(news_p)
```

    Auroras appear on Earth as ghostly displays of colorful light in the night sky, usually near the poles.
    


```python
print(news_title)
```

    NASA's MAVEN Spacecraft Finds That "Stolen" Electrons Enable Unusual Aurora on Mars
    

## JPL Mars Space Image


```python
# Send the browser to the JPL Featured Space Image
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)
```


```python
# Click on FULL IMAGE for the featured image
browser.click_link_by_partial_text('FULL IMAGE')
```


```python
# Click on more info to get to the high quality image
browser.click_link_by_partial_text('more info')
```


```python
# create HTML object
html = browser.html

# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')
```


```python
# Extract URL from the anchor
image_url_pre_formatted = soup.article.figure.a['href']
# Note that the URL is missing the domain
print(image_url_pre_formatted)
```

    /spaceimages/images/largesize/PIA11591_hires.jpg
    


```python
# Create a full link
featured_image_url = 'https://www.jpl.nasa.gov' + image_url_pre_formatted
print(featured_image_url)
```

    https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA11591_hires.jpg
    

## Mars Weather


```python
# Send the browser to the Mars Weather Twitter account
url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)
```


```python
# create HTML object
html = browser.html

# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')
```


```python
# Collect all tweets on the timeline in an iterable list
nearlytimeline = soup.find('div', class_='ProfileTimeline')
timeline = nearlytimeline.find('ol', class_="stream-items js-navigable-stream")
tweetsAll = timeline.find_all('li', class_='js-stream-item stream-item stream-item ')
```


```python
# Iterate through the list indefinitely until a tweet from Mars Weather twitter account appears
# This eliminates the problem of retweets
counter = 0
name = ''

while name != '@MarsWxReport':
    tweet = tweetsAll[counter]
    
    mars_weather = tweet.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    
    tweet_user = tweet.find('span', class_='username u-dir u-textTruncate').text
    
    name = tweet_user
    
    counter += 1

print(mars_weather)
```

    Sol 2108 (2018-07-12), Sunny, high -24C/-11F, low -65C/-84F, pressure at 8.06 hPa, daylight 05:19-17:27
    

## Mars Facts


```python
# Use Pandas to scrape the URL for data formatted as a table
url = 'http://space-facts.com/mars/'

mars_data = pd.read_html(url)
```


```python
# mars_data returns a list so take the 0th element and create a data frame
mars_df = mars_data[0]

mars_df.columns = ['description', 'value']

mars_df.set_index('description', inplace = True)

mars_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>value</th>
    </tr>
    <tr>
      <th>description</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Equatorial Diameter:</th>
      <td>6,792 km</td>
    </tr>
    <tr>
      <th>Polar Diameter:</th>
      <td>6,752 km</td>
    </tr>
    <tr>
      <th>Mass:</th>
      <td>6.42 x 10^23 kg (10.7% Earth)</td>
    </tr>
    <tr>
      <th>Moons:</th>
      <td>2 (Phobos &amp; Deimos)</td>
    </tr>
    <tr>
      <th>Orbit Distance:</th>
      <td>227,943,824 km (1.52 AU)</td>
    </tr>
    <tr>
      <th>Orbit Period:</th>
      <td>687 days (1.9 years)</td>
    </tr>
    <tr>
      <th>Surface Temperature:</th>
      <td>-153 to 20 °C</td>
    </tr>
    <tr>
      <th>First Record:</th>
      <td>2nd millennium BC</td>
    </tr>
    <tr>
      <th>Recorded By:</th>
      <td>Egyptian astronomers</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Convert the data frame to an HTML string
df_html = mars_df.to_html()
```

## Mars Hemispheres


```python
# Initialize an empty list that will be filled with dictionaries
# Initialize a list of the hemispheres so we can loop through and do everything in one cell
hemispheres = ['Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles Marineris']
hemisphere_image_urls = []
```


```python
for hemi in hemispheres:
    # Send the browser to the USGS Astrogeology site to get high res images of the hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    # Do the same as above for Schiaparelli Hemisphere
    browser.click_link_by_partial_text(f'{hemi} Hemisphere Enhanced')

    # create HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Initialize the dict
    hemi_dict = {}

    # Scrape the incomplete URL
    inc_url = soup.find('img', class_='wide-image')['src']

    # Construct the complete URL
    img_url = 'https://astrogeology.usgs.gov' + inc_url

    # Store the data in a dictionary then add that dictionary to the tracking list
    hemi_dict["title"] = f'{hemi} Hemisphere'
    hemi_dict["img_url"] = img_url
    hemisphere_image_urls.append(hemi_dict)
```


```python
hemisphere_image_urls
```




    [{'img_url': 'https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg',
      'title': 'Cerberus Hemisphere'},
     {'img_url': 'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg',
      'title': 'Schiaparelli Hemisphere'},
     {'img_url': 'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg',
      'title': 'Syrtis Major Hemisphere'},
     {'img_url': 'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg',
      'title': 'Valles Marineris Hemisphere'}]


