from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from models import *
from calculations import calculate_total_and_percentage, calculate_arrears_from_am
from datetime import datetime

@login_required
def custom_report(request):
   checktree_data = {}
   checktree_data["departments"] = []
   for dept in Department.objects.all():
      l1_data = []
      for course in Course.objects.filter(department=dept):
         l2_data = []
         for batch in Batch.objects.filter(course=course):
            l2_data.append(batch)
         l1_data.append(("%s(R%d)" % (course.degree, course.regulation.year_formed),l2_data))
      checktree_data["departments"].append((dept.name,dept.abbr,l1_data))
   checktree_data["semesters"] = [("Odd Semester",[1,3,5,7]),("Even Semester",[2,4,6,8])]
   this_year = datetime.now().year
   checktree_data["academic_years"] = [(x,"%d-%d" % (x-1,x)) for x in range(this_year + 1, this_year - 4, -1)]
   if "b" in request.GET and "s" in request.GET and "y" in request.GET:
      b_ids = request.GET.getlist("b")
      semesters = [int(s) for s in request.GET.getlist("s")]
      years = [int(y) for y in request.GET.getlist("y")]
   else:
      return render_to_response('academics/custom_report.html', {'checktree_data':checktree_data}, context_instance=RequestContext(request))
   am1 = AssessmentMark.objects.filter(paper__during_sem__in=semesters)
   am2 = am1.filter(student__batch__id__in=b_ids)
   filtered_am = am2.filter(academic_year__in=years)
   pass_table = ()
   academic_years = ["%d-%d" % (year - 1, year) for year in years]
   selection = {'batches':Batch.objects.filter(id__in=b_ids),'semesters':semesters,'academic_years':academic_years}
   assessed_students = {}
   for marks in filtered_am.all():
      if marks.student not in assessed_students:
         assessed_students[marks.student] = True
      if not marks.isPassed:
         assessed_students[marks.student] = False
   cleared_students = []
   for s in assessed_students.keys():
      if assessed_students[s]:
         cleared_students.append(s)
   assessed_students = assessed_students.keys()
   graphs = {}
   no_all_assessed = len(assessed_students)
   no_all_cleared = len(cleared_students)
   graphs['overall'] = [
                        { 'label': 'Cleared', 'data': no_all_cleared },
                        { 'label': 'Arrear', 'data': no_all_assessed - no_all_cleared + 0.000001}
                       ]
   if no_all_assessed == 0:
      pp_all = 'N/A'
   else:
      pp_all = round((no_all_cleared * 100.0)/no_all_assessed,2)
   pass_table += (('Overall', no_all_assessed, no_all_cleared, pp_all),)
 
   no_male_assessed = 0
   no_male_cleared = 0
   no_female_assessed = 0
   no_female_cleared = 0
   for a_s in assessed_students:
      if a_s.gender == 'M':
         no_male_assessed += 1
      elif a_s.gender == 'F':
         no_female_assessed += 1

   for c_s in cleared_students:
      if c_s.gender == 'M':
         no_male_cleared += 1
      elif c_s.gender == 'F':
         no_female_cleared += 1

   graphs['gender'] = [
                        {'x': 1, 'y': no_male_assessed, 'label': 'Number of Males Appeared', 'color': 'blue'},
                        {'x': 1, 'y': no_male_cleared, 'label': 'Number of Males Cleared', 'color': 'green'},
                        {'x': 3, 'y': no_female_assessed, 'label': 'Number of Females Appeared', 'color': 'purple'},
                        {'x': 3, 'y': no_female_cleared, 'label': 'Number of Females Cleared', 'color': 'pink'},
                      ]
   if no_male_assessed == 0:
      pp_male = 'N/A'
   else:
      pp_male = round((no_male_cleared * 100.0)/no_male_assessed,2)
   if no_female_assessed == 0:
      pp_female = 'N/A'
   else:
      pp_female = round((no_female_cleared * 100.0)/no_female_assessed,2)
   pass_table += (('Male',no_male_assessed,no_male_cleared, pp_male),)
   pass_table += (('Female',no_female_assessed,no_female_cleared, pp_female),)

   no_ds_assessed = 0
   no_ds_cleared = 0
   no_hs_assessed = 0
   no_hs_cleared = 0
   for a_s in assessed_students:
      if a_s.staying == 'D':
         no_ds_assessed += 1
      elif a_s.staying == 'H':
         no_hs_assessed += 1

   for c_s in cleared_students:
      if c_s.staying == 'D':
         no_ds_cleared += 1
      elif c_s.staying == 'H':
         no_hs_cleared += 1

   graphs['staying'] = [
                        {'x': 1, 'y': no_ds_assessed, 'label': 'Number of Dayscholars Appeared', 'color': 'black'},
                        {'x': 1, 'y': no_ds_cleared, 'label': 'Number of Dayscholars Cleared', 'color': '#0ff;'},
                        {'x': 3, 'y': no_hs_assessed, 'label': 'Number of Hostellites Appeared', 'color': 'red'},
                        {'x': 3, 'y': no_hs_cleared, 'label': 'Number of Hostellites Cleared', 'color': 'white'},
                      ]
   if no_ds_assessed == 0:
      pp_ds = 'N/A'
   else:
      pp_ds = round((no_ds_cleared * 100.0)/no_ds_assessed,2)
   if no_hs_assessed == 0:
      pp_hs = 'N/A'
   else:
      pp_hs = round((no_hs_cleared * 100.0)/no_hs_assessed,2)
   pass_table += (('Dayscholars',no_ds_assessed,no_ds_cleared, pp_ds),)
   pass_table += (('Hostellites',no_hs_assessed,no_hs_cleared, pp_hs),)
   no_cs_assessed = 0
   no_cs_cleared = 0
   no_ms_assessed = 0
   no_ms_cleared = 0
   for a_s in assessed_students:
      if a_s.admission == 'C':
         no_cs_assessed += 1
      elif a_s.admission == 'M':
         no_ms_assessed += 1

   for c_s in cleared_students:
      if c_s.admission == 'C':
         no_cs_cleared += 1
      elif c_s.admission == 'M':
         no_ms_cleared += 1

   graphs['admission'] = [
                    {'x': 1, 'y': no_cs_assessed, 'label': 'Number of Counselling Students Appeared', 'color': '#770;'},
                    {'x': 1, 'y': no_cs_cleared, 'label': 'Number of Counselling Students Cleared', 'color': '#ff0;'},
                    {'x': 3, 'y': no_ms_assessed, 'label': 'Number of Management Students Appeared', 'color': '#057'},
                    {'x': 3, 'y': no_ms_cleared, 'label': 'Number of Management Students Cleared', 'color': '#0af'},
                      ]
   if no_cs_assessed == 0:
      pp_cs = 'N/A'
   else:
      pp_cs = round((no_cs_cleared * 100.0)/no_cs_assessed,2)
   if no_ms_assessed == 0:
      pp_ms = 'N/A'
   else:
      pp_ms = round((no_ms_cleared * 100.0)/no_ms_assessed,2)
   pass_table += (('Counselling',no_cs_assessed,no_cs_cleared, pp_cs),)
   pass_table += (('Management',no_ms_assessed,no_ms_cleared, pp_ms),)

   #Toppers (Top 3 overall)
   scores = []
   for c_s in cleared_students:
      student_marks = filtered_am.filter(student=c_s)
      total,percentage = calculate_total_and_percentage(student_marks, c_s.batch.course.regulation.scoring_system)
      scores += [(c_s, percentage, total),]
   toppers = sorted(scores, key=lambda score: score[1], reverse=True)[:3]
   
   toppers_table = ()
   rank = ''
   for topper in toppers:
      rank += 'I'
      toppers_table += ((rank, topper[0].name, topper[0].batch.course.department.abbr, topper[0].reg_no, topper[2], topper[1]),)
      
   # Subjectwise Performance
   subjectwise_passed = ()
   subjectwise_table = ()
   prev_subj = None
   appeared = 0
   passed = 0
   for a_m in filtered_am.order_by('subject__paper__code', 'subject__id'):
      # writing a record after each subject is over
      if prev_subj is not None and prev_subj != a_m.subject:
         if appeared == 0:
            percentage = None
         else:
            percentage = round( (passed * 100.0) / appeared, 2)
         if prev_subj.handled_by is None:
            handled_by = None
         else:
            handled_by = prev_subj.handled_by.name
         subjectwise_passed += ((prev_subj.paper.code, prev_subj.paper.name, appeared, passed, percentage, prev_subj.batch, handled_by),)
         appeared = 0
         passed = 0
      prev_subj = a_m.subject
      if a_m.isPassed:
         passed += 1
      appeared += 1
   if prev_subj is not None:
      if appeared == 0:
         percentage = None
      else:
         percentage = round( (passed * 100.0) / appeared, 2)
      if prev_subj.handled_by is None:
         handled_by = None
      else:
         handled_by = prev_subj.handled_by.name
      subjectwise_passed += ((prev_subj.paper.code, prev_subj.paper.name, appeared, passed, percentage, prev_subj.batch, handled_by),)
      subjectwise_table = sorted(subjectwise_passed, key=lambda row: row[4], reverse=True)
   
   paperwise_failed = ()
   paperwise_table = ()
   prev_paper = None
   appeared = 0
   passed = 0
   for a_m in filtered_am.order_by('paper__code'):
      # writing a record after each paper is over
      if prev_paper is not None and prev_paper != a_m.paper:
         if appeared == 0:
            percentage = None
         else:
            percentage = round( (passed * 100.0) / appeared, 2)
         paperwise_failed += ((prev_paper.code, appeared, appeared - passed, round((appeared-passed)*100.0/appeared,2) or 0),)
         appeared = 0
         passed = 0
      prev_paper = a_m.paper
      if a_m.isPassed:
         passed += 1
      appeared += 1
   if prev_paper is not None:
      if appeared == 0:
         percentage = None
      else:
         percentage = round( (passed * 100.0) / appeared, 2)
      paperwise_failed += ((prev_paper.code, appeared, appeared - passed, round((appeared-passed)*100.0/appeared,2) or 0),)
      paperwise_table = sorted(paperwise_failed, key=lambda row: row[3], reverse=True)

   # Failure distribution
   failure_distribution = {}
   for i in xrange(0,7):
      failure_distribution[i] = 0
   single_paper_failure = {}
   for s in assessed_students:
      filtered_marks = filtered_am.filter(student=s)
      if len(filtered_marks) == 0:
         continue
      no_of_arrears = calculate_arrears_from_am(filtered_marks,True)
      if no_of_arrears in failure_distribution:
         failure_distribution[no_of_arrears] += 1
      else:
         failure_distribution[no_of_arrears] = 1
      # Single Paper Failures
      if no_of_arrears == 1:
         paper = filtered_marks.get(isPassed=False).paper
         if paper in single_paper_failure:
            single_paper_failure[paper] += 1
         else:
            single_paper_failure[paper] = 1
   fd_table = ()
   for i in range(0,7):
      if i in failure_distribution:
         fd_table += ((i,failure_distribution[i]),)
      else:
         fd_table += ((i,0),)
   ssf = ()
   for key,value in sorted(single_paper_failure.iteritems(),key=lambda row: row[1], reverse=True):
      ssf += ((key, value),)
   graphs['failuredistribution'] = [{ 'label': str(i), 'data': failure_distribution[i] + 0.000001 } for i in xrange(0,7) ]
   return render_to_response('academics/custom_report.html', {'selection': selection, 'graphs': graphs, 'pass_table': pass_table, 'toppers_table':toppers_table, 'subjectwise_table':subjectwise_table, 'paperwise_table':paperwise_table, 'fd':fd_table, 'ssf':ssf, 'checktree_data':checktree_data}, context_instance=RequestContext(request))

@login_required
def student_report(request):
   if "Roll_no" not in request.GET:
      return render_to_response('academics/student_report_index.html', context_instance=RequestContext(request))
   student = get_object_or_404(Student, roll_no__iexact=request.GET["Roll_no"])
   semwise_data = []
   for sem_no in range(1,student.batch.course.number_of_semesters + 1):
      ams = student.assessment_marks.filter(paper__during_sem=sem_no)
      semwise_data += [[sem_no,student.get_nth_sem_percentage(sem_no) or 0],]
   aggregate = student.get_aggregate()
   return render_to_response('academics/student_report.html', {'student': student, 'semwise_data': semwise_data, 'aggregate': aggregate}, context_instance=RequestContext(request))
