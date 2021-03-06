import re, json
import mechanize
import urlparse
import urlutil
from bs4 import BeautifulSoup

class BrassringJobScraper(object):
    def __init__(self, url):
        self.br = mechanize.Browser()
        self.url = url
        self.soup = None
        self.jobs = []
        self.numJobsSeen = 0

    def open_search_openings_page(self):
        r = re.compile(r'Search openings', re.I)
        self.br.open(self.url)
        self.br.follow_link(self.br.find_link(text_regex=r))
        
    def soupify_form(self, soup, form_name):
        '''
        Selecting a form with mechanize sometimes throws the error

        'ParseError: OPTION outside of SELECT'

        Running the form through BeautifulSoup seems to fix the issue
        '''
        if not soup:
            soup = BeautifulSoup(self.br.response().read())

        form = soup.find('form', attrs={'name': form_name})
        html = str(form)
        resp = mechanize.make_response(
            html, 
            [("Content-Type", "text/html")],
            self.br.geturl(),
            200, "OK"
        )
        self.br.set_response(resp)

    def submit_search_form(self):
        self.soupify_form(soup=None, form_name='aspnetForm')
        self.br.select_form('aspnetForm')
        self.br.submit()
        self.soup = BeautifulSoup(self.br.response().read())

    def seen_all_jobs(self):
        self.soupify_form(soup=self.soup, form_name='frmMassSelect')
        self.br.select_form('frmMassSelect')
        return self.numJobsSeen >= int(self.br.form['totalrecords'])

    def goto_next_page(self):
        self.br.select_form('frmMassSelect')
        self.br.form.set_all_readonly(False)
        self.br.form['recordstart'] = '%d' % (self.numJobsSeen + 1)
        self.br.submit()
        self.soup = BeautifulSoup(self.br.response().read())

    def scrape_jobs(self):
        while not self.seen_all_jobs():
            t = 'ctl00_MainContent_GridFormatter_json_tabledata'
            i = self.soup.find('input', id=t)
            j = json.loads(i['value'])

            for x in j:
                # debug
                print '\n'.join('%s\t%s' % (y,z) for y,z in x.items())
                print '\n'

                job = {}
                job['title'] = self.get_title_from_job_dict(x)
                job['location'] = self.get_location_from_job_dict(x)
                job['url'] = self.get_url_from_job_dict(x)

                self.jobs.append(job)

            self.numJobsSeen += len(j)

            # Next page
            self.goto_next_page()

    def get_title_from_job_dict(self, job_dict):
        pass

    def get_location_from_job_dict(self, job_dict):
        pass

    def get_soup_anchor_from_job_dict(self, job_dict):
        pass

    def get_url_from_job_dict(self, job_dict):
        a = self.get_soup_anchor_from_job_dict(job_dict)
        u = urlparse.urljoin(self.br.geturl(), a['href'])
        u = self.refine_url(u)
        return u

    def refine_url(self, job_url):
        """
        """
        items = urlutil.url_query_get(
            self.url.lower(), 
            ['partnerid', 'siteid']
        )

        url = urlutil.url_query_filter(job_url, 'jobId')
        url = urlutil.url_query_add(url, items.iteritems())

        return url

    def scrape(self):
        self.open_search_openings_page()
        self.submit_search_form()
        self.scrape_jobs()

