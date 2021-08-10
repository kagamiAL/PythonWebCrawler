#Using urllib module for url functions
import urllib.request

#Get BeautifulSoup module
from bs4 import BeautifulSoup

#To prevent cookie redirect inf loops
from http.cookiejar import CookieJar

#Regex to check if link is a valid url
import re
regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

#Main class
class WebCrawler():
    def __init__(self, URLsToVisit = [], MaxDepth = 10):
        self.__URLsToVisit  = URLsToVisit
        self.__URLsVisited  = set(); 
        self.TraversalMax   = MaxDepth
        self.Paused         = False

    def __AddLinkedURLs(self, tagData):
        if (len(tagData) > 0):
            linksVisited    = self.__URLsVisited
            linksToVisit    = self.__URLsToVisit
            
            for link in tagData:
                newLink = link.get('href')
                if (newLink and re.match(regex, newLink)):
                    if (not newLink in linksVisited and not newLink in linksToVisit):
                        linksToVisit.append(newLink)

    def __Crawl(self):
        #Will visit the current link provided by startUrl or by object's UrlsToVisit
        linksToVisit    = self.__URLsToVisit
        currentLink     = linksToVisit.pop(0)
        print(f"Visiting: {currentLink}")

        try:
            #Requests to visit the provided link while also accounting for redirecting cookies
            urlRequest  = urllib.request.Request(currentLink, headers={'User-Agent': 'Mozilla/5.0'});
            linkOpener  = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()));
            urlResponse = linkOpener.open(urlRequest)

            #The HTML data from the page
            htmlData    = urlResponse.read();

            #Read all urls in the visited Url and appends them to list if traversal length < maxTraversalLength
            if (len(linksToVisit) < self.TraversalMax): 
                self.__AddLinkedURLs(BeautifulSoup(htmlData, 'html.parser').find_all('a'))

            #Close the urlResponse to handle connections
            urlResponse.close();
        except urllib.request.HTTPError as errorMessage:
            return print(format(errorMessage))
        return

    def Destroy(self):
        self.Paused         = True
        self.__URLsToVisit  = []
        self.__URLsVisited  = set()

    def Pause(self):
        self.Paused = True

    def Start(self, startUrl = None):
        linksToVisit = self.__URLsToVisit

        if (startUrl):
            #Checks if the startUrl is a valid link
            if (not re.match(regex, startUrl)): return print("Provided Url is invalid!")
            linksToVisit.append(startUrl);
        elif (len(linksToVisit) == 0):
            return print("Cannot start webcrawler without a StartUrl!")

        currentDepth    = 0

        while (currentDepth < self.TraversalMax and not self.Paused and len(linksToVisit) != 0):
            self.__Crawl();
            currentDepth += 1
        
        stringReport    = ""

        if (not self.Paused):
            stringReport    = "Ended"
            self.Destroy();
        else:
            stringReport    = "Paused"

        print(f"WebCrawler halted, Status = {stringReport}")
