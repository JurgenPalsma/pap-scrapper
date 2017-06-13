# Imports
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


# Container Class that stores an ad's values
class AdContainer(object):
    def __init__(self, price, size, link):
        self.price = price
        self.numPrice = int(price[0:3])
        self.size = size
        self.link = "http://www.pap.fr/" + link

    def dump(self):
        print("Price: " + self.price + " size : " + self.size)

    def dumpAll(self):
        print("Price: " + self.price + "\tsize: " + self.size + "\tlink: " + self.link)


def getCheapestAd(ads):
    cheapestPrice = ads[0].numPrice
    cheapest = ""
    for a in ads:
        if a.numPrice < cheapestPrice:
            cheapestPrice = a.numPrice
    print(cheapestPrice)
def getPageSoupFromFile(path):
    file = open(path, "r")
    r = file.read()
    return (soup(r, "html.parser"))

def getPageSoupFromUrl(url):
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    return (soup(page_html, "html.parser"))

def getAdsFromSelogerPage(url):

#    page_soup = getPageSoupFromFile("./raw.html")
    page_soup = getPageSoupFromUrl(url)
    ads = []

    containers = page_soup.findAll("div", {"class":"box search-results-item"})
    for container in containers:
        price = container.findAll("span", {"class":"price"})
        link = container.findAll("a", {"class":"title-item"})[0]['href']
        surface = container.findAll("strong")
        surf = ""
        for s in surface:
            if "m2" in s.text:
                surf = s.text
        if len(surf) == 0:
            surf = "? m2"
        ads.append(AdContainer(price[0].text,surf,link))

    return ads


#todo make a container class?
#todo sort by most rentable - price / m2 ?


# try:
ads = getAdsFromSelogerPage('http://www.pap.fr/annonce/locations-appartement-paris-75-g439-jusqu-a-500-euros')
ads.extend(getAdsFromSelogerPage('http://www.pap.fr/annonce/locations-appartement-paris-75-g439-jusqu-a-500-euros-2'))
ads.extend(getAdsFromSelogerPage('http://www.pap.fr/annonce/locations-appartement-paris-75-g439-jusqu-a-500-euros-3'))
#ads = getAdsFromSelogerPage("./raw.html")
ads.sort(key = lambda x: x.numPrice)
print("Top 3 cheapest ads:")
ads[0].dumpAll()
ads[1].dumpAll()
ads[2].dumpAll()


#getCheapestAd(ads)
# except:
#     print("Check your connection")
# else:
#     print("Job done")
