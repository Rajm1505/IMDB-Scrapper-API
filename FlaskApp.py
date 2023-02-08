from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
"""
Example Url:
    http://127.0.0.1:5000/scrap?title=Interstellar
"""

@app.route('/scrap', methods = ['GET'])  
def scrapMovie():
    title = request.args.get('title')
    print(title)
    rating = scrap(title)
    if rating == 404:
        return jsonify({'message':"Movie not found"})
    else:
        return jsonify({'rating':rating})

def scrap(title):
    def getSoup(url): 
        headers = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36"}
        page = requests.get(url, headers=headers) 
        print("statuscode: ",page.status_code)
        soup = BeautifulSoup(page.content,'html.parser')
        return soup
    
    print("Processing the request...")

    searchurl = "https://www.imdb.com/find?ref_=nv_sr_fn&q=" + title

    soup = getSoup(searchurl) #Creating a soup for result page after searching for movie
    
    results = soup.find_all('a',class_="ipc-metadata-list-summary-item__t")
    if not results:
        return 404
        
    for result in results:
        movie_page_url = "https://www.imdb.com" + result.get('href')
        break

    print("Movie Page Link: ",movie_page_url)   #Static Example  movie_page_url = "https://www.imdb.com/title/tt0111161/?ref_=fn_al_tt_1"
    print("Now fetching the rating...")
    soup2 = getSoup(movie_page_url) #Soup to extract html from movie page

    
    # search for the element containing the rating information
    rating_element = soup2.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})
    # print(rating_element)

    # retrieve the rating
    try:
        rating = rating_element.find('span')
    except AttributeError:
        return 404
    return rating.string


if __name__ == '__main__':

    app.run(debug=True)