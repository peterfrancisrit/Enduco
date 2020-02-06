from bs4 import BeautifulSoup
import requests
import numpy as np
import pdb

class CyclingCrawler:
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

        print("Crawling")
        # self._write_header() # write the header for tsv file
        self._run()

    def _get_soup(self,url):
        ''' Using BeautifulSoup, function creates a soup object from the url
        param: url
        '''
        try:
            response = requests.get(url)
            self.soup = BeautifulSoup(response.text,"html.parser")
        except:
            print('BAD URL')


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
        ''' Open and write in the log file '''
        with open(self.log,'a') as file:
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

    def _check_endpage(self):
        ''' Cycling tips doesn't return a 404 error, instead has its own error page
        this function attempts to find the error page. Will return true if on error page '''

        return self.soup.find('div',attrs={'class':'et_pb_text_inner'})

    def _run(self):
        ''' Running the webcrawler '''
        try: # Check if in log
            self._check_log()
            print("FROM LATEST ENTRY")
            url, page = self._open_log()
            self.url = self.url[self.url.index(url):] # find latest url to end.
            counter = int(page) # collect the page
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
                    url = URL + "/page/{}/".format(counter)
                    self._get_soup(url)
                counter = 1
        except:
            print("NO ENTRIES IN LOG")
            for URL in self.url:
                counter = 1
                print("URL: {}".format(URL))
                url = URL + "/page/1/"
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
                    url = URL + "/page/{}/".format(counter)
                    self._get_soup(url)


if __name__ == "__main__":
    from url_list import urls
    X = CyclingCrawler(urls)
