from __init__ import *

class ChennaiEducationScraper(Scraper):
   host = "results.chennaieducation.net"

   def get_html(self, reg_no):
      user_agent = 'Mozilla/5 (Ubuntu 10.04) Gecko'
      headers = { 'User-Agent' : user_agent }
      params = urllib.urlencode([('cou', 'result7'),('rollno', reg_no)])
      self.conn.request("POST", "/annauniv/result7.asp", params, headers) # Grade System
      resp = self.conn.getresponse()
      if resp.status == 200:
         return resp.read()
      else:
         raise urllib2.HTTPError(resp.status, resp.reason)

   def parse_html(self, html):
      soup = BeautifulSoup(html)
      trs = soup.findAll('table')[1].findAll('tr')[1:]
      mark_details = {}
      for tr in trs:
         tds = tr.findAll('td')

         # Build the dictionary
         mark_detail = {
            'internal' : tds[1].contents[0].strip(),
            'external' : tds[2].contents[0].strip(),
            'result' : tds[3].contents[0].strip()
         }
         mark_details[tds[0].contents[0].strip()] = mark_detail
      return mark_details
