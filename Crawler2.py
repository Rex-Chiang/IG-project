import requests
import re
import time
import os
import matplotlib.pyplot as plt
from selenium import webdriver
from bs4 import BeautifulSoup as soup
#headers ={
#        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#        'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
#        'cookie':'mcd=3; mid=W6TFzAAEAAEUMIjkAktqtN-uliYt; fbm_124024574287414=base_domain=.instagram.com; csrftoken=sYqGtWAAYTXNPLOFAgSEuYyf01zG3HzG; ds_user_id=344534869; sessionid=344534869%3Aq5ptHXPX2060WX%3A12; shbid=3317; shbts=1554727267.119645; rur=FRC; urlgen="{\"140.116.85.118\": 1659}:1hE8E2:2JXxN3Y8cevC44iQ3_CSVTrW0ug"'
#        }
#for key in headers:
#    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = headers[key]    
#driver = webdriver.PhantomJS(executable_path='/home/rex/桌面/GliaCloud/phantomjs-2.1.1-linux-x86_64/bin/phantomjs', service_log_path = os.path.devnull)

url = "https://www.instagram.com/ss.ling9200/"
html = requests.get(url)
page = soup(html.text,'html.parser')

def PicInfoBEF(page, i):
    
    script = page.find_all("script")[8].text
    script = script.split("shortcode")[i]

    PICre = re.compile(r"(\":\")(https:\/\/[\w\W]*)(\",\"edge_liked_by\")")    
    LIKEre = re.compile(r"(\"edge_liked_by\":{\"count\":)(\d*)")
    COMre = re.compile(r"(\"edge_media_to_comment\":{\"count\":)(\d*)")
    
    getpic = PICre.search(script).group(2)
    getlike = LIKEre.search(script).group(2)
    getcomment = COMre.search(script).group(2)

    return getpic, int(getlike), int(getcomment)

def PicInfoAFT(page, i):
    
    getpic = NextPage.find_all('div',{'class':'KL4Bh'})[i].find('img',{'class':'FFVAD'})["src"]
    getlike = NextPage.find('div',{'class':'Nm9Fw'}).find('span').text
    
    if NextPage.find('li',{'class':'lnrre'}):
        getcomment = NextPage.find('li',{'class':'lnrre'}).find('span').text
    else:
        getcomment = 0
        
    return getpic, int(getlike), int(getcomment)

def Plot(like, comment):
    #LIKES, COMMS = zip(*info.keys())
    plt.plot(like.values(), "bo-", label= "LIKES")
    plt.plot(comment.values(), "ro-", label= "COMMENTS")
    plt.grid(color='g',linestyle='--', linewidth=1,alpha=0.4)
    plt.xlabel("ARTICLES")
    plt.ylabel("COUNTS")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    
    like = dict()
    comment = dict()
    
    driver = webdriver.Chrome(executable_path='/usr/local/share/chromedriver')
    driver.get(url)
    time.sleep(1)
    driver.find_element_by_xpath("//div/a/div[@class='eLAPa']").click()
    time.sleep(1)
    
    for i in range(0, 34):      
        NextPage = soup(driver.page_source,'html.parser')        
        if i < 12:
            getpic, getlike, getcomment = PicInfoBEF(NextPage, i+1)
            like[getpic] = getlike
            comment[getpic] = getcomment
        else:
            getpic, getlike, getcomment = PicInfoAFT(NextPage, i) 
            like[getpic] = getlike
            comment[getpic] = getcomment
            
        driver.find_element_by_xpath("//div/a[@class='HBoOv coreSpriteRightPaginationArrow']").click()
        time.sleep(1)
    
    driver.quit()
        
    Plot(like, comment)







