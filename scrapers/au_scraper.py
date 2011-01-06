from __init__ import *

class AUScraper(Scraper):
   def get_html(self, reg_no):
      user_agent = 'Mozilla/5 (Ubuntu 10.04) Gecko'
      headers = { 'User-Agent' : user_agent }
      params = urllib.urlencode({'regno': reg_no})
      url = "http://result.annauniv.edu/cgi-bin/result/re10.pl?%s" % params
      request = urllib2.Request( url, None, headers)
      response = urllib2.urlopen(request)
      return response.read()

   def parse_html(self, html):
      soup = BeautifulSoup(html)
      trs = soup.find('table').findAll('tr')[2:]
      mark_details = {}
      for tr in trs:
         text = []
         for cell in tr.findAll('center'):
            text.append(cell.contents[0])

         # Build the dictionary
         mark_detail = {
            'internal' : text[1].strip(),
            'external' : text[2].strip(),
            'result' : text[3].strip()
         }
         mark_details[text[0].strip()] = mark_detail
      return mark_details

