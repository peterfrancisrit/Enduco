from bs4 import BeautifulSoup
import requests
import numpy as np
from pyfiglet import Figlet

class Crawler:
    ''' Crawler class for the website "https://cyclingtips.com".
    params: url
    '''
    def __init__(self,url):# max number of pages
        self.file = open("results.txt","a+") # write to file
        self.it = 0 # global iterate
        self.text = "" # store the data
        self.date = "" # store the date
        self.url = url
        self.log = "log.txt"
        self.log_endpage = "log_endpage.txt"
        
        # self._write_header() # write the header for tsv file
        self._run_crawl()

        # Checks new pages crawler needs to run in the beginning
        self._run_newpage_crawl()



    def _get_soup(self,url):
        ''' Using BeautifulSoup, function creates a soup object from the url
        param: url

        :param url: <str> url represented as e.g. https://www.reddit.com/
        '''
        try:
            response = requests.get(url)
            self.soup = BeautifulSoup(response.text,"html.parser")
        except:
            print('CONNECTION LOST OR BAD URL')


    def _get_paras(self):
        ''' private method that collects paragraphs by reading all <p> elements
        a lot of redundancies, however, ensures all text is picked up.
        '''
        paras = self.soup.find_all('p')
        sstring = ''''''
        for text in paras:
            sstring += text.text.replace('\n',' ') + ''' '''
        self.text = sstring

    def _write_paras(self):
        ''' Write the paragraphs from the data '''
        print("{}\0{}".format(self.date,self.text), file=self.file)
        self.it += 1

    def _write_header(self):
        ''' Write the header of the csv file '''
        print("date\0text",file=self.file)

    def _write_log(self,url,page):
        ''' Open and write in the log file

        :param url: <str> takes URL string e.g. https://www.reddit.com/
        :param page: <int> takes page number
        '''
        with open(self.log,'a') as file:
            print("{};{}".format(url,page),file=file)

    def _write_log_endpage(self,url,page):
        with open(self.log_endpage,'a+') as file:
            print("{};{}".format(url,page),file=file)

    def _writeover_log_endpage(self,url,page):
        with open(self.log_endpage,'w+') as file:
            print("{};{}".format(url,page),file=file)

    def _check_log(self):
        ''' Checking the log from current position '''
        with open("log.txt","r+") as file:
            return True

    def _open_log(self):
        ''' Open the log and retrieve the latest entry'''
        with open('log.txt', 'r+') as f:
            lines = f.read().splitlines()
            last_line = lines[-1]
            x = last_line.split(';')
        return x[0], x[1]

    def _open_log_endpage(self):
        ''' Opens the log that contains the endpages for the URL'''
        with open('log_endpage.txt','r+') as f:
            lines = f.read().splitlines()
            URL = [line.split(';')[0] for line in lines]
            ENDPAGE = [line.split(';')[1] for line in lines]

        return URL, ENDPAGE

    def _check_endpage(self):
        ''' Cycling tips doesn't return a 404 error, instead has its own error page
        this function attempts to find the error page. Will return true if on error page '''

        return self.soup.find('div',attrs={'class':'et_pb_text_inner'})

    def _crawl(self,counter=1,stop_when=-1):
        '''Scowers the given URLs using a counter initialised at 1, specify otherwise (when a log
        is present)'''
        if stop_when < 0:
            for URL in self.url:
                url = URL + "/page/{}/".format(counter)
                print("URL: {}".format(URL))
                self._get_soup(url)
                while self.soup.find('div', attrs = {'class':'et_pb_text_inner'}) == None:
                    print("PAGE: {}".format(counter))
                    for sub_url in self.soup.find_all('div',attrs={'class':'ArchiveTilePostGrid__posts-col -clearfix'}):
                        post_urls = sub_url.find_all('div',attrs={'class':'PostSnippet__image'})
                        for post_url in post_urls:
                            self._get_soup(post_url.find('a',href=True)['href'])
                            try:
                                self.date = self.soup.find('p',attrs={'class':'date'}).text
                            except:
                                self.date = "nan"
                            self._get_paras()
                            self._write_paras()
                            if self.it % 50 == 0:
                                print(f"{self.it} texts completed")
                # UPDATE THE URL
                    self._write_log(URL,counter)
                    counter+= 1
                    url = URL + "page/{}".format(counter)
                    self._get_soup(url)

                print("WHY WONT U PRINT THIS")
                self._write_log_endpage(URL,counter - 1)
                counter = 1
        else:
            print("UPDATING...")
            for URL in self.url:
                url = URL + "page/{}/".format(counter)
                print("UPDATING URL: {}".format(URL))
                self._get_soup(url)
                print(counter, stop_when)
                while counter < stop_when + 1:
                    print("PAGE: {}".format(counter))
                    for sub_url in self.soup.find_all('div',attrs={'class':'ArchiveTilePostGrid__posts-col -clearfix'}):
                        post_urls = sub_url.find_all('div',attrs={'class':'PostSnippet__image'})
                        for post_url in post_urls:
                            self._get_soup(post_url.find('a',href=True)['href'])
                            try:
                                self.date = self.soup.find('p',attrs={'class':'date'}).text
                            except:
                                self.date = "nan"
                            self._get_paras()
                            self._write_paras()
                            if self.it % 50 == 0:
                                print(f"{self.it} texts completed")                # UPDATE THE URL
                    counter+= 1
                    url = URL + "/page/{}/".format(counter)
                    self._get_soup(url)

    def _run_crawl(self):
        ''' Running the webcrawler '''
        try: # Check if in log
            self._check_log()
            print("RUNNING FROM LATEST ENTRY")
            url, page = self._open_log()
            self.url = self.url[self.url.index(url):] # find latest url to end.
            counter = int(page) # collect the page
            self._crawl(counter + 1,-1)
            counter = 1

        except:
            print("NO ENTRIES IN LOG")
            self._crawl()

    def _run_newpage_crawl(self):
        ''' Checks and runs the crawler on new pages from the last log entries '''
        self.url, endpages = self._open_log_endpage()
        new_endpage = []
        print(self.url)
        for url, endpage in zip(self.url,endpages):
            URL = url + 'page/{}'.format(int(endpage) + 1)
            self._get_soup(URL)
            print(URL)
            new_page = 1

            while self.soup.find('div', attrs = {'class':'et_pb_text_inner'}) == None:
                URL = url + 'page/{}'.format(int(endpage) + new_page)
                self._get_soup(URL)
                new_page += 1
                self._crawl(1,new_page)

            new_endpage.append(new_page + int(endpage) - 1)

        print(new_endpage)
        for url, endpage in zip(self.url, new_endpage):
            self._writeover_log_endpage(url,endpage)
