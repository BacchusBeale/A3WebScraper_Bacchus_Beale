# http://www.environment.gov.au/cgi-bin/sprat/public/publicthreatenedlist.pl?wanted=fauna
# http://zetcode.com/python/beautifulsoup/#:~:text=BeautifulSoup%20is%20a%20Python%20library,%2C%20navigable%20string%2C%20or%20comment.
# https://www.youtube.com/watch?v=ng2o98k983k
# https://www.pluralsight.com/guides/web-scraping-with-beautiful-soup

import requests
from bs4 import BeautifulSoup
import csv

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

    def extractMainTable(self, saveAsCSV):
        try:
            csvheader = ["category", "hyperlink", "fauna"]
            print(csvheader)
            datalist = []

            table = self.soup.find(id="threatsummary")
            rows = table.find_all('tr')
            
            for row in rows:
                print("row:",row)
                th = row.th
                category = th.get_text()
                td = row.find('td')
                anchor = td.find_all('a')
                # total row has no links only summary
                if (anchor is None) or (len(anchor)==0):
                    total = ["Total", "", td.get_text()]
                    datalist.append(total)
                for item in anchor:
                    print("item:",item)
                    link = item['href']
                    fauna = item.get_text()                       
                    datum = [category,link,fauna]
                    print("Next: ",datum)
                    datalist.append(datum)

            # debug
            print("datalist: ", datalist)

            # if empty not including header
            if len(datalist)<2:
                raise BaseException("Get data error")

            # https://docs.python.org/3/library/csv.html
            with open(saveAsCSV, 'w', newline='') as f:
                csvwriter = csv.writer(f, delimiter=',')
                csvwriter.writerow(csvheader)
                for data in datalist:
                    csvwriter.writerow(data)

        except BaseException as e:
            print(f"Error: {str(e)}")
            return False
        return True

    def showPageHeaders(self):
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
        spider.showPageHeaders()
        spider.extractMainTable(saveAsCSV="maintable.csv")
    else:
        print("Can't load website")
    

if __name__ == "__main__":
    runSpider()