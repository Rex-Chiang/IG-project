#from selenium import webdriver
import requests
import re
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as soup

url = "https://www.instagram.com/rickys_cookingdiary/"

html = requests.get(url)
page = soup(html.text,'html.parser')

script = page.find_all("script")[4].text

def RE(content):

    FOLLOWre = re.compile(r"(edge_followed_by\":{\"count\":)(\d*)")
    FOLLOWEDre = re.compile(r"(edge_follow\":{\"count\":)(\d*)")
    ARTICLEre = re.compile(r"(edge_owner_to_timeline_media\":{\"count\":)(\d*)")
    
    followers = FOLLOWre.search(content).group(2)
    followed = FOLLOWEDre.search(content).group(2)
    article = ARTICLEre.search(content).group(2)
    
    return followers, followed, article

followers, followed, article = RE(script)

def ProInfo(content):
    
    like = dict()
    comment = dict()
    PROre = re.compile(r"(profile_pic_url_hd\":\")(https:\/\/[\w\W]*)(\",\"requested_by_viewer\")")    
    LIKEre = re.compile(r"(https:\/\/[\w\W]*)(\",\"edge_liked_by\":{\"count\":)(\d*)")
    COMre = re.compile(r"(edge_media_to_comment\":{\"count\":)(\d*)")
    content = content.split("shortcode")
    
    for article in content:
                
        getlike = LIKEre.search(article)
        getcomment = COMre.search(article)
 
        if getlike != None:            
            like[getlike.group(1)] = int(getlike.group(3))
            comment[ getlike.group(1)] = int(getcomment.group(2))
        else:
            pro = PROre.search(article)
            pro = pro.group(2)
    
    return pro, like, comment

def Plot(like, comment):
    #LIKES, COMMS = zip(*info.keys())
    plt.plot(like.values(), "bo-", label= "LIKES")
    plt.plot(comment.values(), "ro-", label= "COMMENTS")
    plt.grid(color='g',linestyle='--', linewidth=1,alpha=0.4)
    plt.xlabel("ARTICLES")
    plt.ylabel("COUNTS")
    plt.legend()
    plt.show()
    
pro, like, comment = ProInfo(script)
Plot(like, comment)

def Statistic(like, comment):
    TransLike = {v : k for k, v in like.items()}
    TransComm = {v : k for k, v in comment.items()}

    Most_Liked_Posts = TransLike[max(like.values())]
    Most_Commented_Posts = TransComm[max(comment.values())]
    Least_Liked_Posts = TransLike[min(like.values())]
    Least_Commented_Posts = TransComm[min(comment.values())]
    
    return Most_Liked_Posts, Most_Commented_Posts, Least_Liked_Posts, Least_Commented_Posts

Most_Liked_Posts, Most_Commented_Posts, Least_Liked_Posts, Least_Commented_Posts = Statistic(like, comment)