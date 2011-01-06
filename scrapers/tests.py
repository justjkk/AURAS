from chennai_education_scraper import ChennaiEducationScraper
from au_scraper import AUScraper
import sys
from utilities import parse_reg_nos
import simplejson as json

if __name__ == "__main__":
   if len(sys.argv) != 2:
      print "Usage:python %s <file_containing_register_numbers>" % sys.argv[0]
      sys.exit()
   f = open(sys.argv[1],'r')
   reg_str = f.read()
   reg_index = parse_reg_nos(reg_str)
   scraper = AUScraper()
   all_students_mark_details = scraper.do_scrape(reg_index)
   # Output the Dictionary to json file
   f = open('output.json','w')
   f.write(json.dumps(all_students_mark_details, indent=4, sort_keys=True))
   f.close()

   # Output the Dictionary to stdout as json
   #print json.dumps(all_students_mark_details, indent=4, sort_keys=True)
