from __init__ import *

class AUScraper(Scraper):
   host = "result.annauniv.edu"

   def get_html(self, reg_no):
      user_agent = 'Mozilla/5 (Ubuntu 10.04) Gecko'
      headers = { 'User-Agent' : user_agent }
      params = urllib.urlencode({'regno': reg_no})
      self.conn.request("GET", "/cgi-bin/result/re10.pl?%s" % params, None, headers) # Mark System
      #self.conn.request("GET", "/cgi-bin/result/result10gr.pl?%s" % params) # Grade System
      resp = self.conn.getresponse()
      if resp.status == 200:
         return resp.read()
      else:
         raise Exception("%d:%s" % (resp.status, resp.reason))

   def parse_html(self, html):
      soup = BeautifulSoup(html)
      trs = soup.find('table').findAll('tr')[2:]
      if len(trs) == 0:
         raise Exception("Register number does not probably exist")
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

