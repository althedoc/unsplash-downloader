from selenium import webdriver
import time
import requests
import os
import shutil


# Change this for the main page on Unsplash that you wish to grab images from
mainurl = "https://unsplash.com/t/wallpapers"

# Linux format - this is where to store the images
outputdir = "/home/MYUSERNAME/Desktop/wallpapersUnsplash"

# Number of times to scroll down automatically in the webbrowser - 14 is a good starting point
numberofscrollsdown = 14
scrolldownpixels = 1000


# Remove and then create the output folder

if os.path.isdir(outputdir)==True:
    shutil.rmtree(outputdir)            # remove folder and all its files
os.mkdir(outputdir)


# windows:
#browser = webdriver.Chrome("C:/chromedriver.exe")

# Goto: https://github.com/mozilla/geckodriver/releases
# Copy the latest webdriver executable to /usr/bin     (for firefox, must be in same folder as firefox executable)
browser = webdriver.Firefox()
browser.get(mainurl)

y = scrolldownpixels
for x in range(0, numberofscrollsdown):
    browser.execute_script("window.scrollTo(0, "+str(y)+")")
    y += scrolldownpixels
    time.sleep(1)

el = browser.find_elements_by_tag_name("a")
for elm in el:
    elref = elm.get_attribute("href")
    if "/photos/" in elref:
        if not "/download?force=true" in elref:
            #print(elref)
            image_url = elref + "/download?force=true&w=1920"
            
            r = requests.get(image_url, allow_redirects=True)
            filename = r.headers.get('content-disposition')
            flnm1 = filename.replace('attachment;filename="', '')
            flnm2 = flnm1.replace('"', '')
            with open (outputdir+"/"+flnm2, "wb") as f:
                f.write(r.content)            


print ("All done!")           
