from BeautifulSoup import BeautifulSoup
import urllib2
import urllib
import simplejson as json
from sys import stderr

failure_tries_left = 5 # Give a non-zero value or 0 for no limit

user_agent = 'Mozilla/5 (Ubuntu 10.04) Gecko'
headers = { 'User-Agent' : user_agent }
reg_index = range(31107104001, 31107104125)
reg_index += range(31107104300, 31107104315)

# Scrape the Marks information for every reg_no in reg_index
all_students_mark_details = {}

for reg_no in reg_index:
   # GET the mark details from the server
   try:
       params = urllib.urlencode({'regno': reg_no})
       url = "http://result.annauniv.edu/cgi-bin/result/re10.pl?%s" % params
       request = urllib2.Request( url, None, headers)
       response = urllib2.urlopen(request)
       html = response.read()
   except Exception,e:
       stderr.write(e)
       failure_tries_left -= 1
       if failure_tries_left == 0: break
       continue

   # Parse the HTML   
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
   if len(mark_details) != 0:
      all_students_mark_details[reg_no] = mark_details

# Output the Dictionary to json file
f = open('cse7thsem.json','w')
f.write(json.dumps(all_students_mark_details, indent=4, sort_keys=True))
f.close()

# Output the Dictionary to stdout as json
print json.dumps(all_students_mark_details, indent=4, sort_keys=True)

