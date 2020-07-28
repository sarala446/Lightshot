from urllib.request import urlretrieve, urlopen, Request
from bs4 import BeautifulSoup
import random, string, os
import threading
import time

DIRNAME = "Output"
DLCOUNT = 0
ERCOUNT = 0
LENGTH = 6

class LightShot(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):

        while True:
            fileName = self.generateId(LENGTH)
            url = self.generateLink(fileName)
            print(url)
            self.generateImgur(url, fileName)

    def generateLink(self, fileName):
        return "https://prnt.sc/" + fileName


    def generateId(self, size):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(size))


    def generateHtml(self, fileName):
        url = self.generateLink(fileName)
        request = Request(url, headers={'User-Agent': 'Chrome/5.0'})
        print(request)
        page = urlopen(request).read()
  
        return page

    def generateImgur(self, url, fileName):
        soup = BeautifulSoup(self.generateHtml(fileName), 'html.parser')
        imgUrl = soup.find('img', id='screenshot-image')['src']

        if imgUrl != '//st.prntscr.com/2018/06/19/0614/img/0_173a7b_211be8ff.png':
            global DLCOUNT
            DLCOUNT += 1
            archive_path = DIRNAME + "/" + fileName + ".png"
            urlretrieve(imgUrl, archive_path)
            print("File: " + fileName + " - Saved to " + DIRNAME + " folder.  ")
            print("Total Number of Downloads: " + str(DLCOUNT))

        else:
            global ERCOUNT
            ERCOUNT += 1
            print("The requested url is invalid. Trying a new combination... Error n. " + str(ERCOUNT))


def main():

    if not os.path.exists(DIRNAME):
        os.makedirs(DIRNAME)

    for _ in range(int(input("Please enter the number of threads to be used: "))):
        thread = LightShot()
        thread.start()
        time.sleep(0.25)

        print("Threads in active : {}".format(threading.activeCount() - 1))


main()



