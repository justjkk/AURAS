from pyExcelerator import *
import os
import sys

def setup_environment():
    pathname = os.path.dirname(sys.argv[0])
    sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '..')))
    sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '../..')))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

def get_batch(batchstr): # batchstr format: B.E. CSE A 2011
   from academics.models import Batch
   degree, department, section, year_of_graduation = batchstr.split(' ')
   batch = Batch.objects.filter(course__degree=degree).filter(course__department__abbr=department).filter(year_of_graduation=year_of_graduation).get(section=section)
   return batch
   
def student_details_from_xls(xls):
   student_details = {}
   record = {}
   prev_row_idx = 0
   prev_sheet_name = None
   for sheet_name, values in parse_xls(xls):
      if sheet_name not in student_details:
         student_details[sheet_name] = []
      for row_idx, col_idx in sorted(values.keys()):
         if row_idx == 0: continue
         if prev_row_idx != row_idx and prev_row_idx != 0:
            student_details[sheet_name].append(record)
            record = {}
         record[values[(0,col_idx)]] = values[(row_idx, col_idx)]
         prev_row_idx = row_idx
      if prev_row_idx != 0: student_details[sheet_name].append(record)
   return student_details

"""
"" student_details format: {"B.E. CSE A 2011": [{"RollNo":"07CS001",...},...],...}
"""
def update_student_details(student_details):
   from academics.models import Student
   for batch_name in student_details:
      batch = get_batch(batch_name)
      for record in student_details[batch_name]:
         try:
            student = Student.objects.get(roll_no=record['RollNo'])
            if student.batch != batch:
               raise Exception("Student '%s' doesn't belong to batch '%s'" % (record['RollNo'],batch_name))
         except Student.DoesNotExist:
            student = Student()
            student.roll_no = record['RollNo']
            student.batch = batch
         if 'RegNo' in record: student.reg_no = str(int(record['RegNo']))
         if 'Admission' in record: student.admission = record['Admission']
         if 'Staying' in record: student.staying = record['Staying']
         if 'Gender' in record: student.gender = record['Gender']
         if 'StudentName' in record: student.name = record['StudentName']
         student.save()

def bulk_uploader(src):
   if src.__class__.__name__ == 'InMemoryUploadedFile':
      temp = open(src.name, 'wb+')
      for chunk in src.chunks():
         temp.write(chunk)
      temp.close()
      fname = src.name
   else:
      fname = src
   extn = fname.rsplit(".",1)[-1].lower()
   if extn == "xls":
      student_details = student_details_from_xls(fname)
   elif extn == "csv":
      pass #TODO: Implement student_details_from_csv(fname)
   elif extn == "xml":
      pass #TODO: Implement student_details_from_xml(fname)
   else:
      if src.__class__.__name__ == 'InMemoryUploadedFile': os.remove(src.name)
      raise Exception("Unknown file extension '%s'" % extn)
   if src.__class__.__name__ == 'InMemoryUploadedFile': os.remove(src.name)
   update_student_details(student_details)

if __name__ == "__main__":
   setup_environment()
   if len(sys.argv) != 2:
      print "Usage: python %s <xls/csv/xml source>" % sys.argv[0]
      sys.exit()
   bulk_uploader(sys.argv[1])
