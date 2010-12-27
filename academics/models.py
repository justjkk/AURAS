from django.db import models
from django.db.models.signals import post_save
from calculations import *

GENDER_CHOICES = (
   ('M','Male'),
   ('F','Female'),
)

ADMISSION_CHOICES = (
   ('C','Counselling'),
   ('M','Management'),
)

STAYING_CHOICES = (
   ('D','Day Scholar'),
   ('H','Hostelite'),
)

DESIGNATION_CHOICES = (
   ('HD','Head of the Department'),
   ('P' ,'Professor'),
   ('AP','Assistant Professor'),
   ('SL','Senior Lecturer'),
   ('L' ,'Lecturer'),
)

SCORING_SYSTEM_CHOICES = (
   ('G', 'Grade System'),
   ('M', 'Mark System'),
)

GRADE_CHOICES = (
   (10, 'S'),
   (9, 'A'),
   (8, 'B'),
   (7, 'C'),
   (6, 'D'),
   (5, 'E'),
   (0, 'U'),
)

class RegulationManager(models.Manager):
   def get_by_natural_key(self, year_formed):
      return self.get(year_formed=year_formed)

class Regulation(models.Model):
   objects = RegulationManager()
   year_formed = models.IntegerField(unique=True)
   scoring_system = models.CharField(max_length=1, choices=SCORING_SYSTEM_CHOICES, default='G')

   def natural_key(self):
      return (self.year_formed,)

   def __unicode__(self):
      return 'R' + str(self.year_formed)

class DepartmentManager(models.Manager):
   def get_by_natural_key(self, abbr):
      return self.get(abbr=abbr)

class Department(models.Model):
   objects = DepartmentManager()
   name = models.CharField(max_length=100)
   abbr = models.CharField(max_length=4, unique=True)
   def natural_key(self):
      return (self.abbr,)

   def __unicode__(self):
      return self.abbr

class CourseManager(models.Manager):
   def get_by_natural_key(self, degree, department__abbr, regulation__year_formed):
      return self.get(degree=degree, department__abbr=department__abbr, regulation__year_formed=regulation__year_formed)

class Course(models.Model):
   objects = CourseManager()
   degree = models.CharField(max_length=100)
   number_of_semesters = models.IntegerField(default=8)
   department = models.ForeignKey(Department)
   regulation = models.ForeignKey(Regulation)
   class Meta:
      unique_together = ['degree', 'department', 'regulation']
   def natural_key(self):
      return (self.degree, self.department.abbr, self.regulation.year_formed)

   def __unicode__(self):
      return self.degree + ' ' + self.department.abbr + ' ' + str(self.regulation)
   
class Faculty(models.Model):
   
   # Required fields
   name = models.CharField(max_length=100)
   department = models.ForeignKey(Department)

   # Contact profile
   address = models.CharField(max_length=250, null=True, blank=True)
   phone_no = models.CharField(max_length=12, null=True, blank=True)
   email_id = models.EmailField(null=True, blank=True)
   
   # College profile
   designation = models.CharField(max_length=2, choices=DESIGNATION_CHOICES, null=True, blank=True)
   date_of_joining = models.DateField(null=True, blank=True)
   salary = models.IntegerField(null=True, blank=True)
   
   # Education profile
   qualification = models.CharField(max_length=50, null=True, blank=True)
   experience = models.SmallIntegerField(null=True, blank=True)

   def __unicode__(self):
      return self.name

class PaperManager(models.Manager):
   def get_by_natural_key(self, code, course__degree, course__department__abbr, course__regulation__year_formed):
      return self.get(code=code, course__degree=course__degree, course__department__abbr=course__department__abbr, course__regulation__year_formed=course__regulation__year_formed)

class Paper(models.Model): # Paper <- Theory/Lab Paper
   objects = PaperManager()
   code = models.CharField(max_length=8) # Code is not unique as the same subject code can be shared by papers of different courses. Resisting normalization of code->name relationship
   name = models.CharField(max_length=100)
   course = models.ForeignKey(Course)
   during_sem = models.SmallIntegerField()
   credits = models.IntegerField(null=True, blank=True)
   
   class Meta:
      unique_together = ['code', 'course']
   
   def natural_key(self):
      return (self.code, self.course.degree, self.course.department.abbr, self.course.regulation.year_formed)
   
   def __unicode__(self):
      return self.code + ' | ' + self.name
      
   def save(self, *args, **kwargs):
      if self.course.regulation.scoring_system == 'G' and credits == None:
         raise Exception('Credit cannot be None because the course uses Grading System')
      super(Paper, self).save(args, kwargs)

class BatchManager(models.Manager):
   def get_by_natural_key(self, course__department__abbr, year_of_graduation, section):
      return self.get(course__department__abbr=course__department__abbr, year_of_graduation=year_of_graduation, section=section)

class Batch(models.Model): # Batch <- Class

   objects = BatchManager()
   course = models.ForeignKey(Course)
   year_of_graduation = models.IntegerField()
   section = models.CharField(max_length=1)
   class_teacher = models.ForeignKey(Faculty, unique=True, null=True, blank=True)

   class Meta:
      unique_together = ['course', 'year_of_graduation', 'section']

   def natural_key(self):
      return (self.course.department.abbr, self.year_of_graduation, self.section)

   def __unicode__(self):
      return self.course.department.abbr + '-' + self.section + '-' + (str)(self.year_of_graduation)

class SubjectManager(models.Manager):
   def get_by_natural_key(self, paper__code, batch__course__department__abbr, batch__year_of_graduation, batch__section):
      return self.get(paper__code=paper__code, batch__course__department__abbr=batch__course__department__abbr, batch__year_of_graduation=batch__year_of_graduation, batch__section=batch__section )

class Subject(models.Model):
   objects = SubjectManager()   
   paper = models.ForeignKey(Paper, null=True, blank=True)  
   batch = models.ForeignKey(Batch)
   handled_by = models.ForeignKey(Faculty, null=True, blank=True)
      
   class Meta:
      unique_together = ['paper','batch']
      ordering = ['paper__name',]

   def natural_key(self):
      return (self.paper.code, self.batch.course.department.abbr, self.batch.year_of_graduation, self.batch.section)

   def __unicode__(self):
      return str(self.paper.name) + ' | ' + str(self.batch)

class StudentManager(models.Manager):
   def get_by_natural_key(self, roll_no):
      return self.get(roll_no=roll_no)

class Student(models.Model):
   objects = StudentManager()
   
   # Personal profile
   name = models.CharField(max_length=100)
   gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
   admission = models.CharField(max_length=1, choices=ADMISSION_CHOICES, null=True, blank=True)
   staying = models.CharField(max_length=1, choices=STAYING_CHOICES, null=True, blank=True)
   
   # Contact profile
   address = models.CharField(max_length=250, null=True, blank=True)
   phone_no = models.CharField(max_length=12, null=True, blank=True)
   email_id = models.EmailField(null=True, blank=True)
   
   # College profile
   roll_no = models.CharField(max_length=8, unique=True)
   batch = models.ForeignKey(Batch)
   college_status = models.BooleanField(default=True)
   
   # University profile
   reg_no = models.CharField(max_length=11, null=True, blank=True)
   university_status = models.BooleanField(default=True)
   
   aggregate = models.FloatField(null=True, blank=True, editable=False)
   standing_arrears = models.IntegerField(null=True, blank=True, editable=False)
   history_of_arrears = models.IntegerField(null=True, blank=True, editable=False)

   class Meta:
      ordering = ['roll_no']
   
   def natural_key(self):
      return (self.roll_no,)
   
   def __unicode__(self):
      return self.roll_no+' | '+self.name
   
   def get_aggregate(self):
      return calculate_aggregate(self)
      
   def get_nth_sem_percentage(self, sem):
      return calculate_nth_sem_percentage(self, sem)
   
   def get_nth_sem_total(self, sem):
      return calculate_nth_sem_total(self, sem)

   def get_nth_sem_arrears(self, sem):
      return calculate_nth_sem_arrears(self, sem)
      
   def get_standing_arrears(self):
      return calculate_standing_arrears(self)

   def get_history_of_arrears(self):
      return calculate_history_of_arrears(self)
      
   def save(self, *args, **kwargs):
      super(Student, self).save(args, kwargs)
      self.aggregate = self.get_aggregate()
      self.standing_arrears = self.get_standing_arrears()
      self.history_of_arrears = self.get_history_of_arrears()
      super(Student, self).save()

class AssessmentMark(models.Model):
   student = models.ForeignKey(Student, related_name='assessment_marks')
   paper = models.ForeignKey(Paper)
   internal_mark = models.IntegerField()
   external_mark = models.IntegerField(null=True, blank=True, help_text='For Mark System only')
   external_grade = models.IntegerField(choices=GRADE_CHOICES, null=True, blank=True, help_text='For Grade System only')
   isPassed = models.NullBooleanField(null=True, blank=True, editable=False)
   attempt = models.IntegerField(null=True, blank=True, editable=False)
   latest_attempt = models.BooleanField(default=True, editable=False)
   academic_year = models.IntegerField(null=True, blank=True, editable=False)
   subject = models.ForeignKey(Subject, null=True, blank=True, editable=False)
   
   def save(self, *args, **kwargs):
      if self.paper.course.regulation.scoring_system == 'M': # Mark System
         if self.external_mark is None:
            raise Exception("External mark is empty but the Paper belongs to Mark System")
         if self.external_mark < 36 or self.internal_mark + self.external_mark < 50:
            self.isPassed = False
         else:
            self.isPassed = True
      elif self.paper.course.regulation.scoring_system == 'G': # Grade System
         if self.external_grade is None:
            raise Exception("External Grade is empty but the Paper belongs to Grade System")
         if self.get_external_grade_display() == 'U':
            self.isPassed = False
         else:
            self.isPassed = True
      self.academic_year = self.student.batch.year_of_graduation - self.paper.course.number_of_semesters / 2 + (self.paper.during_sem + 1) / 2
      self.subject = Subject.objects.filter(paper=self.paper).get(batch=self.student.batch)
      super(AssessmentMark,self).save(args, kwargs)
      if self.attempt is None:
         prev_attempt = AssessmentMark.objects.filter(student=self.student).filter(paper=self.paper).filter(latest_attempt=True).exclude(pk=self.pk)
         if len(prev_attempt) == 0:
            self.attempt = 1
         else:
            prev_attempt = prev_attempt[0]
            self.attempt = prev_attempt.attempt + 1
            prev_attempt.latest_attempt = False
            prev_attempt.save()
         super(AssessmentMark,self).save()
      self.student.save()

   def __unicode__(self):
      return str(self.student.roll_no) + ' scored ' + str(self.internal_mark) + ', ' + str(self.external_mark) + ' in ' + str(self.paper.code) + ' | Attempt: '+ str(self.attempt)
