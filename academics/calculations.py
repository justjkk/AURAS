#Contains all the business logic for calculating student aggregates, etc...

def calculate_total_and_percentage(assessment_marks, scoring_system):
   if scoring_system == 'G': # Grade system
      ''' Calculate GPA * 10 '''
      total_scored = 0
      total_credits = 0
      for am in assessment_marks.filter(latest_attempt=True):
         total_scored += am.internal_mark
         total_scored += ( am.subject.credits * am.external_grade )
         total_credits += am.subject.credits
      if total_credits == 0:
         return None,None
      percentage = round(float(total_scored) / total_credits,2) * 10
   elif scoring_system == 'M': # Mark system
      ''' Calculate Percentage '''
      total_scored = 0
      total_subjects = 0
      for am in assessment_marks:
         total_scored += am.internal_mark
         total_scored += am.external_mark
         total_subjects += 1
      if total_subjects == 0:
         return None,None
      percentage = round(float(total_scored) / total_subjects,2)
   return total_scored,percentage

def calculate_aggregate(student):
   assessment_marks = student.assessment_marks.all()
   scoring_system = student.batch.course.regulation.scoring_system
   return calculate_total_and_percentage(assessment_marks, scoring_system)[1]

def calculate_nth_sem_percentage(student, semester):
   assessment_marks = student.assessment_marks.filter(paper__during_sem=semester)
   scoring_system = student.batch.course.regulation.scoring_system
   return calculate_total_and_percentage(assessment_marks, scoring_system)[1]

def calculate_nth_sem_total(student, semester):
   assessment_marks = student.assessment_marks.filter(paper__during_sem=semester)
   scoring_system = student.batch.course.regulation.scoring_system
   return calculate_total_and_percentage(assessment_marks, scoring_system)[0]
   
def calculate_arrears_from_am(assessment_marks,want_history):
   if want_history:
      return len(assessment_marks.filter(isPassed=False))
   else:
      return len(assessment_marks.filter(isPassed=False).filter(latest_attempt=True))

def calculate_standing_arrears(student):
   return calculate_arrears_from_am(student.assessment_marks, False)

def calculate_history_of_arrears(student):
   return calculate_arrears_from_am(student.assessment_marks, True)
