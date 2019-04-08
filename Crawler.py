#from selenium import webdriver
import requests
import re
from bs4 import BeautifulSoup as soup

url = "https://www.instagram.com/rickys_cookingdiary/"

html = requests.get(url)
page = soup(html.text,'html.parser')

script = page.find_all("script")[4].text

def RE(content):

    FOLLOWre = re.compile(r"(edge_followed_by\":{\"count\":)(\d*)")
    FOLLOWEDre = re.compile(r"(edge_follow\":{\"count\":)(\d*)")
    ARTICLEre = re.compile(r"(edge_owner_to_timeline_media\":{\"count\":)(\d*)")
    LIKEre = re.compile(r"(edge_liked_by\":{\"count\":)(\d*)")
    
    followers = FOLLOWre.search(content).group(2)
    followed = FOLLOWEDre.search(content).group(2)
    article = ARTICLEre.search(content).group(2)
    likes = LIKEre.findall(content)
    
    return followers, followed, article, likes

followers, followed, article, likes = RE(script)

for like in likes:
    print(like[1])


