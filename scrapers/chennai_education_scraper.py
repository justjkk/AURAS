from __init__ import *

class ChennaiEducationScraper(Scraper):

   def get_html(self, reg_no):
      user_agent = 'Mozilla/5 (Ubuntu 10.04) Gecko'
      headers = { 'User-Agent' : user_agent }
      url = "http://results.chennaieducation.net/annauniv/result7.asp"
      data = urllib.urlencode([('cou', 'result7'),('rollno', reg_no)])
      request = urllib2.Request( url, None, headers)
      response = urllib2.urlopen(request, data)
      return response.read()

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
