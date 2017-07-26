import requests
import sys
import traceback
import time
from random import choice
from bs4 import BeautifulSoup
from bs4 import NavigableString
from urlparse import urljoin
import csv
from multiprocessing import Pool
import multiprocessing
import copy
import re
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from selenium.common.exceptions import TimeoutException


HOST="localhost"
USER="root"
PASS="admin"
DBNAME="item_report"

reload(sys)  
sys.setdefaultencoding('utf8')

cols = []

#-*-coding:utf-8-*-
    
def crawl ():
    result = {}
    HEADERS_MAP = {}
    cols = {"Location","Info","Image"}
    for header in cols:
        HEADERS_MAP[header] = header
    csv_writer = csv.DictWriter(outputCsv, fieldnames = cols, extrasaction='ignore')
    csv_writer.writerow(HEADERS_MAP)

    driver.get("https://www.meetup.com/find/sports-fitness/?allMeetups=false&radius=50&userFreeform=Kuala+Lumpur%2C+Malaysia&mcId=c1028906&mcName=Kuala+Lumpur%2C+MY&sort=default")
    

    while True:
        src = driver.page_source # gets the html source of the page
        soup = BeautifulSoup(src,"lxml") 
        films = soup.find_all("li", class_="groupCard tileGrid-tile")
        if films:
#            driver.find_element_by_link_text('ENG').click()
#            time.sleep(1)
#            src = driver.page_source
#            soup = BeautifulSoup(src,"lxml") 
#            films = soup.find_all("div", class_="showtime-box movie-box-bycinema")
            break

        time.sleep(1)

    for film in films:
        location = film["data-name"]        

        datas = film.find("a", class_="groupCard--photo loading nametag-photo ")
        data_url = datas["href"]
        image_data = datas["style"]
        startpos = image_data.find("(")
        endpos = image_data.find(")")            
        image_url = image_data[startpos+1:endpos]        
        
        info = film.find("p", class_="small ellipsize")

#        driver.get(data_url)
#        src = driver.page_source
#        soup = BeautifulSoup(src,"lxml")
#        meetsups = soup.find_all("div", class_="unit size4of5")

        print location.encode('ascii',errors='ignore')
        print "   Image:  " + image_url
        print "    Info:  " + ''.join(info.text.split())

        time_data = get_soup_from_url(data_url)
        if time_data != None:
            lists = time_data.find_all("div", class_="unit size4of5")
            for list in lists:
                time = list.find("p", class_="margin-none")
                loc = list.find("h3", class_="big")
                print "    time:  " + time.text
                print "        :  " + loc.text

        print "  "
        print "  "
        print "  "

#        info = info.text.replace('\n', '')
#        info = info.replace('\n', '')

#        print "Location:" + location +"     Info:" + ''.join(info.text.split()) + "    ImageURL:" + image_url 
        


if __name__ == '__main__':
    outputFile = "D:\\Scrap\\pgm.csv"
    driver = webdriver.Firefox()
    outputCsv = open(outputFile,'wb')
    crawl()
    outputCsv.close()
    driver.quit()
    