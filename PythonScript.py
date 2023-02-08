import requests 
from bs4 import BeautifulSoup 
import time

def getSoup(url):
    headers = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36"}
    page = requests.get(url, headers=headers) 
    print("statuscode: ",page.status_code)
    soup = BeautifulSoup(page.content,'html.parser')
    return soup
    
title = input("Enter the title: ")
print("Processing the request...")
start = time.time()

searchurl = "https://www.imdb.com/find?ref_=nv_sr_fn&q=" + title

soup = getSoup(searchurl)
results = soup.find_all('a',class_="ipc-metadata-list-summary-item__t")

for result in results:
    movie_page_url = "https://www.imdb.com" + result.get('href')
    break

print("Movie Page Link: ",movie_page_url)
#Static Example  movie_page_url = "https://www.imdb.com/title/tt0111161/?ref_=fn_al_tt_1"
print("Now fetching the rating...")
soup2 = getSoup(movie_page_url)
# search for the element containing the rating information
rating_element = soup2.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})
# print(rating_element)
# retrieve the rating
rating = rating_element.find('span')
print("rating:",rating.string)
end = time.time()

print(f"time taken: {end-start} ")

