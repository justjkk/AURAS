import os
import sys

def setup_environment():
   pathname = os.path.dirname(sys.argv[0])
   sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '..')))
   sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '../..')))
   os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

if __name__ == "__main__":
   setup_environment()
   from academics.models import Batch, Subject, StudentSubject
   for batch in Batch.objects.all():
      for paper in batch.course.papers.all():
         if paper.is_lab_paper:
            subject1 = Subject.objects.get_or_create(paper=paper, batch=batch, lab_batch=1)[0]
            subject2 = Subject.objects.get_or_create(paper=paper, batch=batch, lab_batch=2)[0]
            for student in batch.students.all():
               if student.lab_batch == 1:
                  StudentSubject.objects.get_or_create(student=student, subject=subject1)
               else: # student.lab_batch == 2:
                  StudentSubject.objects.get_or_create(student=student, subject=subject2)
         else:
            subject = Subject.objects.get_or_create(paper=paper, batch=batch, lab_batch=1)[0]
            for student in batch.students.all():
               StudentSubject.objects.get_or_create(student=student, subject=subject)
