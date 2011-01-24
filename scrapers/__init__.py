import urllib
import httplib
import urllib2
from BeautifulSoup import BeautifulSoup
from sys import stderr
import sys
from abc import ABCMeta, abstractmethod

class Scraper():
   __metaclass__ = ABCMeta

   @abstractmethod
   def get_html(self, reg_no):
      return NotImplemented

   @abstractmethod
   def parse_html(self, html):
      return NotImplemented

   host = None
   conn = None

   def do_scrape(self, reg_index, debug=False):
      all_students_mark_details = {}
      self.conn = httplib.HTTPConnection(self.host)
      for reg_no in reg_index:
         if debug:
            stderr.write("%d\n" % reg_no)
         try:
            html = self.get_html(reg_no)
         except Exception, e:
            stderr.write("Error retrieving results for Reg.no %s. Error was '%s'\n" % (reg_no, e.__str__()))
            continue
         try:
            mark_details = self.parse_html(html)
            if len(mark_details) != 0:
               all_students_mark_details[reg_no] = mark_details
         except Exception, e:
            stderr.write("Error processing results for Reg.no %s. Error was '%s'\n" % (reg_no, e.__str__()))
            continue
      self.conn.close()
      return all_students_mark_details
