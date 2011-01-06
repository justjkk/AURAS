import urllib
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

   def do_scrape(self, reg_index):
      all_students_mark_details = {}
      for reg_no in reg_index:
         try:
            html = self.get_html(reg_no)
         except urllib2.HTTPError, e:
            stderr.write(e.__str__())
         try:
            mark_details = self.parse_html(html)
            if len(mark_details) != 0:
               all_students_mark_details[reg_no] = mark_details
         except Exception, e:
            stderr.write("Error processing Reg.no %s. Error was %s" % (reg_no, e))
      return all_students_mark_details
