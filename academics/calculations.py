#Contains all the business logic for calculating student aggregates, etc...

def calculate_pass_or_fail(scoring_system, internal_mark, external_score):
   if scoring_system == 'M': # Mark System
      if external_score < 36 or internal_mark + external_score < 50:
         return False
      return True
   elif scoring_system == 'G': # Grade System
      if external_score < 5:
         return False
      return True
   raise Exception("Scoring System(%s) is Unknown" % scoring_system)

def calculate_total_and_percentage(student_subjects, scoring_system):
   if scoring_system == "M":
      total_mark = 0
      total_subjects = 0
      for ss in student_subjects:
         if ss.number_of_attempts > 0:
            total_mark += ss.internal_mark
            total_mark += ss.external_score
            total_subjects += 1
      if total_subjects == 0:
         return None, None
      return total_mark, round(float(total_mark) / total_subjects, 2)
   else: # student.batch.course.regulation.scoring_system == "G":
      total_grade = 0
      total_credits = 0
      for ss in student_subjects:
         if ss.number_of_attempts > 0:
            credits = ss.subject.paper.credits
            total_grade += ss.external_score * credits
            total_credits += credits
      if total_credits == 0:
         return None, None
      return total_grade, round(total_grade * 10.0 / total_credits, 3)

def calculate_aggregate(student):
   student_subjects = student.student_subjects
   scoring_system = student.batch.course.regulation.scoring_system
   return calculate_total_and_percentage(student_subjects, scoring_system)[1]

def calculate_nth_sem_percentage(student, semester):
   student_subjects = student.student_subjects.filter(subject__paper__during_sem=semester)
   scoring_system = student.batch.course.regulation.scoring_system
   return calculate_total_and_percentage(student_subjects, scoring_system)[1]

def calculate_nth_sem_total(student, semester):
   student_subjects = student.student_subjects.filter(subject__paper__during_sem=semester)
   scoring_system = student.batch.course.regulation.scoring_system
   return calculate_total_and_percentage(student_subjects, scoring_system)[0]

def calculate_standing_arrears(student):
   return student.student_subjects.filter(is_passed=False).count()

def calculate_history_of_arrears(student):
   return student.student_subjects.filter(number_of_attempts__gt=1).count()

