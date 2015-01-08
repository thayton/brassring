import urllib
import urlparse

def url_query_add(url, items):
    """
    Add items to query portion of url
    """
    u = urlparse.urlparse(url)
    qs = urlparse.parse_qs(u.query)

    for k,v in items:
        qs[k] = v

    u = list(u)
    u[4] = urllib.urlencode(qs, doseq=True)
    return urlparse.urlunparse(u)

def url_query_del(url, keys):
    """
    Remove items from query portion of url whose keys are in keys parameter
    """
    u = urlparse.urlparse(url)
    qs = urlparse.parse_qs(u.query)

    if isinstance(keys, str):
        keys = [ keys ]

    for k in keys:
        if qs.has_key(k):
            del(qs[k])

    u = list(u)
    u[4] = urllib.urlencode(qs, doseq=True)
    return urlparse.urlunparse(u)

def url_query_get(url, keys):
    """
    Return items (as a dictionary) from query whose keys appear in keys parameter
    """
    u = urlparse.urlparse(url)
    qs = urlparse.parse_qs(u.query)

    if isinstance(keys, str):
        keys = [ keys ]

    for k in qs.keys():
        if k not in keys:
            del(qs[k])

    return dict([ (x,y[0]) for x,y in qs.items() ])

def url_query_filter(url, keys):
    """
    Filter out any item whose key does not appear in keys
    """
    u = urlparse.urlparse(url)
    qs = urlparse.parse_qs(u.query)

    if isinstance(keys, str):
        keys = [ keys ]

    for k in qs.keys():
        if k not in keys:
            del(qs[k])

    u = list(u)
    u[4] = urllib.urlencode(qs, doseq=True)
    return urlparse.urlunparse(u)

def url_params_del(url):
    u = urlparse.urlparse(url)
    u = list(u)
    u[3] = None
    return urlparse.urlunparse(u)

def url_set_path(url, path):
    u = urlparse.urlparse(url)
    u = list(u)
    u[2] = path
    return urlparse.urlunparse(u)
    
def url_domain(url):
    """
    Extract domain from url
    """
    u = urlparse.urlparse(url)
    n = u.netloc.split(':')[0]
    d = '.'.join(n.split('.')[-2:])

    return d

if __name__ == '__main__':
    jobs_page_url = 'https://jobs.brassring.com/en/asp/tg/cim_home.asp?sec=1&partnerid=119&siteid=69'
    job_url = 'https://jobs.brassring.com/en/asp/tg/cim_jobdetail.asp?SID=^SU7_slp_rhc_IeohzQM1yovos57JiqSvFYhrGfTAsIa8qZbbvZK558PE1aEixA==&jobId=1230473&type=search&JobReqLang=1&recordstart=1&JobSiteId=69&JobSiteInfo=1230473_69&GQId=238'

    res = url_query_filter(job_url, 'jobId')
    items = url_query_get(jobs_page_url, ['partnerid', 'siteid'])
    res = url_query_add(res, items.iteritems())

    print res
