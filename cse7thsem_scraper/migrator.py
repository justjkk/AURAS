import simplejson as json
import os
import sys
def setup_env():
   pathname = os.path.dirname(sys.argv[0])
   sys.path.append(os.path.abspath(pathname))
   sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '..')))
   sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '../..')))
   os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
setup_env()
from academics.models import Student, AssessmentMark, Paper

def update_marks(marks_dict):
   unprocessed = {}
   for reg_no in marks_dict.keys():
      for subject_code in marks_dict[reg_no].keys():
         try:
            mark = marks_dict[reg_no][subject_code]
            student = Student.objects.get(reg_no=reg_no)
            paper = Paper.objects.filter(code=subject_code).get(course=student.batch.course)
            am = AssessmentMark()
            am.student = student
            am.paper = paper
            am.internal_mark = int(mark["internal"])
            am.external_mark = int(mark["external"]) # External mark, are you sure?
            am.save()
         except Exception, e:
            if not unprocessed.has_key(reg_no):
               unprocessed[reg_no] = {}
            unprocessed[reg_no][subject_code] = mark
            print "Error updating mark of Reg.No:%s, Sub.Code:%s (%s)" % (reg_no, subject_code, e)
   if len(unprocessed.keys()):
      print "Unprocessed"
      print json.dumps(unprocessed, indent=4, sort_keys=True)

if __name__ == "__main__":
   if len(sys.argv) != 2:
      print "Usage: python %s <marks_dict_file>" % sys.argv[0]
      sys.exit()
   marks_file = open(sys.argv[1], "r")
   marks_json = json.load(marks_file)
   update_marks(marks_json)
