# Mission to Mars Scraping
This exercise was to practice HTML/CSS scraping on a series of websites concerning data from Mars.

## Deliverable 1
Code to isolate hemisphere data is as follows:
```
# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
hemi_soup = soup(html, 'html.parser')

hemi_elem = hemi_soup.find_all('div', class_='item')

for hemi in hemi_elem:
    hemi_data = {}
    
    # Find URL to hemisphere page
    hemi_url_rel = hemi.find('a').get('href')
    
    # Navigate to Hemisphere page, set up new Soup
    browser.visit(f"{url}{hemi_url_rel}")
    hemi_html = browser.html
    hemi_image_soup = soup(hemi_html, 'html.parser')
    
    # Isolate <div> tag for box with download information
    hemi_image_box = hemi_image_soup.find('div', class_='downloads')
    
    # Find URL to first link, which is the full "Sample" link and assign to dictionary
    hemi_image_url_rel = hemi_image_box.find('a', target='_blank').get('href')
    hemi_data['img_url'] = f"{url}{hemi_image_url_rel}"
    
    # Find title, assign to dictionary
    hemi_title = hemi_image_soup.find('h2', class_='title').get_text()
    hemi_data['title'] = hemi_title
    
    # Append data to list of dictionaries and browser back
    hemisphere_image_urls.append(hemi_data)
    browser.back()
```
## Deliverable 2
- Implemented mars_hemis() function from Deliverable 1 to scrape the hemisphere data.
- Updated index.html template to use "mars.image_dicts", which is what I named my list of dictionaries.
## Deliverable 3
### Updates to improve look and function in mobile devices
1. In the index.html template, I changed each image class from "col-md-6" to "col-xs-6 col-md-6" to allow images to be displayed 2x2 on a mobile device.
2. In the scraping.py file, I added to the Mars Facts return statement, to replace the table's class of "dataframe" with a bootstrap-enabled 'table table-striped'
'''
return df.to_html().replace('dataframe','table table-striped')
'''
3. In the index.html template, I added the "active" tag to the "Scrape New Data" button, so that the user can see when the scraping is in progress and then finished.
4. In the index.html template, I 'swapped' the header sizes of the "Mars Facts" text and the hemisphere caption texts, so that, particularly for mobile devices, "Mars Facts" is a bit more noticable and the hemisphere captions fit better.
