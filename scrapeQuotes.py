import json
import requests
from bs4 import BeautifulSoup

data_arr = [] # array to save objects to

def getSoup(page_url): # make request to page_url and provide soup
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def getContents(soup): # find and retrieve all items of interest and save to data_arr
    divs = soup.find_all("div", class_="quote")

    for div in divs:
        quote = div.find("span", class_="text").get_text(strip=True)
        author = div.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in div.find_all("a", class_="tag")]

        data_arr.append({
            "quote": quote,
            "author": author,
            "tags": tags
        })

def getNextPage(soup): # iterate over all available pages
    links = [a for a in soup.find_all('a') if "Next" in a.get_text()]
    if len(links) > 0:
        link = links[0]["href"]
        return "https://quotes.toscrape.com" + link
    return None

url = "https://quotes.toscrape.com"

while url: # actual scraping
    soup = getSoup(url)
    getContents(soup)
    url = getNextPage(soup)

print(f"Total quotes collected: {len(data_arr)}")
print(data_arr[:3])

# save file
with open("/Users/moritzbecker/Desktop/scrapedQuotes.json", "w", encoding="utf8") as file:
    json.dump(data_arr, file, indent=4, ensure_ascii=False)