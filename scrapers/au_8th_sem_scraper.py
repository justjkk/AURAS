from __init__ import *

class AU8thSemScraper(Scraper):
   host = "result.annauniv.edu"

   def get_html(self, reg_no):
      user_agent = 'Mozilla/5 (Ubuntu 10.04) Gecko'
      headers = { 'User-Agent' : user_agent }
      params = urllib.urlencode({'regno': reg_no})
      self.conn.request("GET", "/cgi-bin/result/revre09.pl?%s" % params, None, headers) # Mark System
      resp = self.conn.getresponse()
      if resp.status == 200:
         return resp.read()
      else:
         raise urllib2.HTTPError(resp.status, resp.reason)

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
         if text[0].strip() == "8TH SEMESTER RESULTS WILL BE PUBLISHED ALONG WITH THE LOWER SEMESTER RESULTS":
            continue
         mark_details[text[0].strip()] = mark_detail
      return mark_details

