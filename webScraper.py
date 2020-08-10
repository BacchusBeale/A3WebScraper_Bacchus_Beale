# http://www.environment.gov.au/cgi-bin/sprat/public/publicthreatenedlist.pl?wanted=fauna
# http://zetcode.com/python/beautifulsoup/#:~:text=BeautifulSoup%20is%20a%20Python%20library,%2C%20navigable%20string%2C%20or%20comment.
# https://www.youtube.com/watch?v=ng2o98k983k

import requests
from bs4 import BeautifulSoup

class EnvironmentSpider:
    def __init__(self):
        self.main_url = ""
        self.main_page = None
        self.soup = None

    def loadMainPage(self, webaddress):
        try:
            self.main_url=webaddress
            page = requests.get(self.main_url)
            self.main_page = page.text
        except BaseException as e:
            print(f"Load page error: {str(e)}")
            return False
        return True

    def loadFromFile(self, filename='page.html'):
        try:
            with open(filename, 'r') as f:
                text = f.read()
                self.main_page=text
        except BaseException as e:
            print(f"Load page error: {str(e)}")
            return False
        return True

    def saveHtml(self, filename='page.html'):
        try:
            with open(filename, "w") as f:
                f.write(str(self.soup))
        except BaseException as e:
            print(f"Save page error: {str(e)}")
            return False
        return True
        
    def parseMainPage(self):
        try:
            self.soup = BeautifulSoup(self.main_page, 'html.parser')
        except BaseException as e:
            print(f"parse page error: {str(e)}")
            return False
        return True

    def getMainHeader(self):
        try:
            mainHeader=""
            match = self.soup.find('div', class_="app-heading")
            #print("match=", type(match))
            if match is not None:
                mainHeader = match.h1.get_text()
            return mainHeader
        except BaseException as e:
            return f"Error {str(e)}"
        
    def getContentHeader(self):
        try:
            subHeader=""
            match = self.soup.find(id="top")
            #print("match=", type(match))
            if match is not None:
                subHeader = match.get_text()
            return subHeader
        except BaseException as e:
            return f"Error {str(e)}"

    def scrape(self):
        heading = self.getMainHeader()
        print(f"Main Heading: {heading}")
        sub = self.getContentHeader()
        print(f"Sub Heading; {sub}")


import os

def runSpider():
    weburl = "http://www.environment.gov.au/cgi-bin/sprat/public/publicthreatenedlist.pl?wanted=fauna"
    htmlFile = 'endangeredFauna.html'
    spider = EnvironmentSpider()

    ok=False
    if os.path.exists(htmlFile):
        print("Load from file")
        ok = spider.loadFromFile(filename=htmlFile)
        if ok:
            ok = spider.parseMainPage()
            print(f"Page parsed = {ok}")
    else:
        print("Load from web")
        ok = spider.loadMainPage(webaddress=weburl)
        if ok:
            ok = spider.parseMainPage()
            print(f"Page parsed = {ok}")
            if ok:
                ok = spider.saveHtml(filename=htmlFile)
                print(f"Html saved = {ok}")
    
    if ok:
        print("Web scraping started...")
        spider.scrape()
    
    else:
        print("Can't load website")
    
# https://www.pluralsight.com/guides/web-scraping-with-beautiful-soup
if __name__ == "__main__":
    runSpider()