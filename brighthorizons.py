#!/usr/bin/env python

import sys, signal
from brassring import BrassringJobScraper
from bs4 import BeautifulSoup

# BrightHorizons
URL = 'https://sjobs.brassring.com/TGWebHost/home.aspx?partnerid=25595&siteid=5216'

def sigint(signal, frame):
    sys.stderr.write('Exiting...\n')
    sys.exit(0)    

class BrightHorizonsJobScraper(BrassringJobScraper):
    def __init__(self):
        super(BrightHorizonsJobScraper, self).__init__(url=URL)        

    def get_title_from_job_dict(self, job_dict):
        t = job_dict['FORMTEXT13']
        t = BeautifulSoup(t)
        return t.text

    def get_location_from_job_dict(self, job_dict):
        l = job_dict['FORMTEXT12'] + ', ' + job_dict['FORMTEXT8']
        l = l.strip()
        return l

    def get_soup_anchor_from_job_dict(self, job_dict):
        t = job_dict['FORMTEXT13']
        t = BeautifulSoup(t)
        return t.a

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint)

    scraper = BrightHorizonsJobScraper()
    scraper.scrape()

    for j in scraper.jobs:
        print j
