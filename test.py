import requests
import re
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as soup

url = "https://www.instagram.com/p/Bv4NlYxgn1c/"

html = requests.get(url)
page = soup(html.text,'html.parser')

script = page.find_all("script")[4].text

def ProInfo(content):
    
    like = dict()
    comment = dict()
    
    PICre = re.compile(r"(\"src\":\")(https:\/\/[\w\W]*)(\",\"config_width\")")    
    LIKEre = re.compile(r"(\"userInteractionCount\":\")(\d*)")
    COMre = re.compile(r"(\"edge_media_to_parent_comment\":{\"count\":)(\d*)")
    
    getpic = PICre.search(content)
    getlike = LIKEre.search(content)
    getcomment = COMre.search(content)
             
    like[getpic] = int(getlike.group(2))
    comment[getpic] = int(getcomment.group(2))

    return like, comment

like, comment = ProInfo(script)

print(like)
print(comment)