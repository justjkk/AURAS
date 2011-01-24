from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete
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
   department = models.ForeignKey(Department, related_name='courses')
   regulation = models.ForeignKey(Regulation, related_name='courses')
   class Meta:
      unique_together = ['degree', 'department', 'regulation']
   def natural_key(self):
      return (self.degree, self.department.abbr, self.regulation.year_formed)

   def __unicode__(self):
      return self.degree + ' ' + self.department.abbr + ' ' + str(self.regulation)
   
class Faculty(models.Model):
   fac_id = models.CharField(max_length=10)
   name = models.CharField(max_length=100)
   department = models.ForeignKey(Department, related_name='faculties')

   def __unicode__(self):
      return self.fac_id + ' | ' + self.name

class PaperManager(models.Manager):
   def get_by_natural_key(self, code, course__degree, course__department__abbr, course__regulation__year_formed):
      return self.get(code=code, course__degree=course__degree, course__department__abbr=course__department__abbr, course__regulation__year_formed=course__regulation__year_formed)

class Paper(models.Model): # Paper <- Theory/Lab Paper
   objects = PaperManager()
   code = models.CharField(max_length=8) # Code is not unique as the same subject code can be shared by papers of different courses. code->name relationship is denormalized here
   name = models.CharField(max_length=100)
   course = models.ForeignKey(Course, related_name='papers')
   during_sem = models.SmallIntegerField()
   credits = models.IntegerField(null=True, blank=True)
   is_lab_paper = models.BooleanField(default=False)
   
   class Meta:
      unique_together = ['code', 'course']
   
   def natural_key(self):
      return (self.code, self.course.degree, self.course.department.abbr, self.course.regulation.year_formed)
   
   def __unicode__(self):
      return self.code + ' | ' + self.name
   
   def clean(self):
      if self.course.regulation.scoring_system == 'G' and self.credits is None:
        raise ValidationError("Credit cannot be None in Grade System.")

   '''
   def save(self, *args, **kwargs):
      self.clean()
      super(Paper, self).save(args, kwargs)
   '''

class BatchManager(models.Manager):
   def get_by_natural_key(self, course__degree, course__department__abbr, year_of_graduation, section):
      return self.get(course__degree=course__degree, course__department__abbr=course__department__abbr, year_of_graduation=year_of_graduation, section=section)

class Batch(models.Model): # Batch <- Class

   objects = BatchManager()
   course = models.ForeignKey(Course, related_name='batches')
   year_of_graduation = models.IntegerField()
   section = models.CharField(max_length=1)

   class Meta:
      unique_together = ['course', 'year_of_graduation', 'section']

   def natural_key(self):
      return (self.course.degree, self.course.department.abbr, self.year_of_graduation, self.section)

   def __unicode__(self):
      return self.course.department.abbr + '-' + self.section + '-' + (str)(self.year_of_graduation)

class SubjectManager(models.Manager):
   def get_by_natural_key(self, paper__code, batch__course__department__abbr, batch__year_of_graduation, batch__section, lab_batch):
      return self.get(paper__code=paper__code, batch__course__department__abbr=batch__course__department__abbr, batch__year_of_graduation=batch__year_of_graduation, batch__section=batch__section, lab_batch=lab_batch)

class Subject(models.Model):
   objects = SubjectManager()   
   paper = models.ForeignKey(Paper, related_name='subjects')
   batch = models.ForeignKey(Batch, related_name='subjects')
   handled_by = models.ForeignKey(Faculty, null=True, blank=True, related_name='subjects_handled')
   hours_spent = models.IntegerField(null=True, blank=True)
   lab_batch = models.IntegerField(default=1,choices=((1,'I'),(2,'II'))) # 1 for theory subjects, 1 or 2 for lab subjects

   class Meta:
      unique_together = ['paper','batch','lab_batch']
      ordering = ['paper__name',]

   def natural_key(self):
      return (self.paper.code, self.batch.course.department.abbr, self.batch.year_of_graduation, self.batch.section, self.lab_batch)

   def __unicode__(self):
      return str(self.paper.name) + ' | ' + str(self.batch)

   def clean(self):
      if self.paper.course != self.batch.course:
         raise ValidationError("Paper(%s) is not allowed as a Subject for Batch(%s)" % (self.paper, self.batch))

   '''
   def save(self, *args, **kwargs):
         self.clean()
         super(Subject, self).save(args, kwargs)
   '''

class StudentManager(models.Manager):
   def get_by_natural_key(self, roll_no):
      return self.get(roll_no=roll_no)

class Student(models.Model):
   objects = StudentManager()
   
   name = models.CharField(max_length=100)
   gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
   admission = models.CharField(max_length=1, choices=ADMISSION_CHOICES, null=True, blank=True)
   staying = models.CharField(max_length=1, choices=STAYING_CHOICES, null=True, blank=True)

   roll_no = models.CharField(max_length=8, unique=True)
   reg_no = models.BigIntegerField(null=True, blank=True)
   batch = models.ForeignKey(Batch, related_name='students')
   lab_batch = models.IntegerField(choices=((1,'I'),(2,'II'))) # Lab batches are assumed to be exactly 2
   subjects = models.ManyToManyField(Subject, through='StudentSubject')
   
   # Calculated Fields
   aggregate = models.FloatField(null=True, blank=True, editable=False)
   standing_arrears = models.IntegerField(null=True, blank=True, editable=False)
   history_of_arrears = models.IntegerField(null=True, blank=True, editable=False)

   class Meta:
      ordering = ['roll_no']
   
   def natural_key(self):
      return (self.roll_no,)
   
   def __unicode__(self):
      return self.roll_no + ' | ' + self.name
   
   def get_aggregate(self):
      if self.aggregate is None:
         self.aggregate = calculate_aggregate(self)
      return self.aggregate
      
   def get_nth_sem_percentage(self, sem):
      return calculate_nth_sem_percentage(self, sem)
   
   def get_nth_sem_total(self, sem):
      return calculate_nth_sem_total(self, sem)

   def get_nth_sem_arrears(self, sem):
      return calculate_nth_sem_arrears(self, sem)
      
   def get_standing_arrears(self):
      if self.standing_arrears is None:
         self.standing_arrears = calculate_standing_arrears(self)
      return self.standing_arrears

   def get_history_of_arrears(self):
      if self.history_of_arrears is None:
         self.history_of_arrears = calculate_history_of_arrears(self)
      return self.history_of_arrears
      
   def recalculate(self):
      self.aggregate = calculate_aggregate(self)
      self.standing_arrears = calculate_standing_arrears(self)
      self.history_of_arrears = calculate_history_of_arrears(self)
      self.save()

class StudentSubject(models.Model):
   student = models.ForeignKey(Student, related_name='student_subjects')
   subject = models.ForeignKey(Subject, related_name='student_subjects')
   internal_mark = models.IntegerField(null=True, blank=True, help_text='For Mark System only')
   hours_attended = models.IntegerField(null=True, blank=True)
   # Calculated Fields
   is_passed = models.NullBooleanField(null=True, blank=True, editable=False)
   number_of_attempts = models.IntegerField(default=0, editable=False)
   external_score = models.ForeignKey('ExternalScore', null=True, blank=True, editable=False)

   def clean(self):
      if self.student.batch != self.subject.batch:
         raise ValidationError("Student(%s) cannot take Batch(%s)'s subject(%s)" % (self.student, self.subject.batch, self.subject) )
      if self.student.batch.course.regulation.scoring_system == 'M' and self.internal_mark is None:
         raise ValidationError("Internal Mark cannot be Null for Mark System")
   def __unicode__(self):
      return ""
   '''
   def save(self, *args, **kwargs):
      self.clean()
      super(StudentSubject,self).save(args, kwargs)
   '''

class ExternalScore(models.Model):
   student_subject = models.ForeignKey(StudentSubject, related_name='external_scores')
   score = models.IntegerField() # Can store either External Mark[0..100] / External Grade[0..10]
   
   # Calculated Fields
   is_passed = models.BooleanField(default=False, editable=False)
   attempt = models.IntegerField(null=True, blank=True, editable=False)

   def clean(self):
      if self.student_subject.is_passed == True:
         raise ValidationError("External Score(%d) cannot be added to Student's Subject(%s) which is passed already." % (self.external_score, self.student_subject))

   def save(self, *args, **kwargs):
      '''
      self.clean()
      '''
      scoring_system = self.student_subject.student.batch.course.regulation.scoring_system
      self.student_subject.is_passed = self.is_passed = calculate_pass_or_fail(scoring_system, self.student_subject.internal_mark, self.score)
      #self.academic_year = self.student.batch.year_of_graduation - self.paper.course.number_of_semesters / 2 + (self.paper.during_sem + 1) / 2
      if self.attempt is None:
         self.student_subject.number_of_attempts += 1
         self.student_subject.external_score = self
         self.student_subject.save()
      super(ExternalScore,self).save(args, kwargs)
   
   def __unicode__(self):
      return "Student(%s) scored %d in Subject(%s) - Attempt %d" % ( self.student_subject.student, self.student_subject.subject, self.attempt )

def external_score_pre_delete(**kwargs):
   external_score = kwargs['instance']
   student_subject = external_score.student_subject
   external_score.student_subject.number_of_attempts -= 1
   external_score.student_subject.external_score = None #FIXME: Assign to prev attempts
   external_score.student_subject.external_score.save()

pre_delete.connect(external_score_pre_delete, sender=ExternalScore)
