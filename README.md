# PythonWebCrawler

DISCLAIMER: This will only work if you have BeautifulSoup 4 installed

This is the first python project that I've ever done, so please don't expect a lot from it :)

Credits to Ari Bajo and his web crawler guide, https://www.scrapingbee.com/blog/crawling-python/, for guiding me along with the creation of this project

//DOCUMENTATION

  - WebCrawler(URLsToVisit : list, MaxDepth : number)
    //URLsToVisit (OPTIONAL): This is a parameter that takes in a list of links the web crawler will visit
    //MaxDepth: This parameter accepts a number that the web crawler will use to restrict the number of links it visits
    
  - WebCrawler.Start(StartURL) (This method starts the web crawler)
    //StartURL (Is optional if you have paused the web crawler): Where the web crawler will start its journey
  
  - WebCrawler.Pause() (This method pauses the web crawler)
    
  - WebCrawler.Destroy() (This method cleans up the stored links the object holds and pauses the web crawler)
