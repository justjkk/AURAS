from __init__ import *

class WorldCollegesInfoScraper(Scraper):
   host = "www.worldcolleges.info"

   def get_html(self, reg_no):
      user_agent = 'Mozilla/5 (Ubuntu 10.04) Gecko'
      headers = { 'User-Agent' : user_agent }
      params = urllib.urlencode({'regno': reg_no})
      self.conn.request("GET", "/results-all/anna_univ_2011_Jan/anna_display.php?%s" % params, None, headers)
      resp = self.conn.getresponse()
      if resp.status == 200:
         html = resp.read()
         if html.find("Check your Register Number") != -1:
            raise Exception("Register Number does not exist")
         return html
      else:
         raise Exception("%d:%s" % (resp.status, resp.reason))

   def parse_html(self, html):
      soup = BeautifulSoup(html)
      trs = soup.findAll('table')[1].findAll('tr')[2:]
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

