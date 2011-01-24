from chennai_education_scraper import ChennaiEducationScraper
from au_scraper import AUScraper
from world_colleges_info import WorldCollegesInfoScraper
import sys
from utilities import parse_reg_nos
import simplejson as json
import argparse

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description='Invokes different scrapers for a discontinuous\
                              range of register numbers passed in a text file or stdin(default)')
   parser.add_argument('-d', '--debug',
                       help='Debug flag. Writes verbose messages to stderr',
                       action='store_true')
   scrapers = parser.add_mutually_exclusive_group(required=True)
   scrapers.add_argument('-au', '--anna-university', action='store_true',
                         help='Scrape from Anna University Results Site')
   scrapers.add_argument('-ce', '--chennai-education', action='store_true',
                         help='Scrape from ChennaiEducation.net')
   scrapers.add_argument('-wc', '--world-colleges-info', action='store_true',
                         help='Scrape from WorldColleges.info')
   parser.add_argument('-i','--input', dest='reglist', 
                         help='Input filename containing register numbers',
                         metavar='<input_filename>')
   ns = parser.parse_args(sys.argv[1:])
   if ns.reglist is None:
      f = sys.stdin
   else:
      f = open(ns.reglist, 'r') or sys.stdin
   reg_str = f.read()
   reg_index = parse_reg_nos(reg_str)
   if ns.anna_university:
      scraper = AUScraper()
   elif ns.chennai_education:
      scraper = ChennaiEducationScraper()
   elif ns.world_colleges_info:
      scraper = WorldCollegesInfoScraper()
   all_students_mark_details = scraper.do_scrape(reg_index, debug=ns.debug)
   
   # Output the Dictionary to json file
   #f = open('output.json','w')
   #f.write(json.dumps(all_students_mark_details, indent=4, sort_keys=True))
   #f.close()

   # Output the Dictionary to stdout as json
   print json.dumps(all_students_mark_details, indent=4, sort_keys=True)
