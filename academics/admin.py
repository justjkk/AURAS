from models import *
from django.contrib import admin

class StudentSubjectInline(admin.TabularInline):
   model = StudentSubject
   readonly_fields = ('student','subject')

class StudentAdmin(admin.ModelAdmin):
   list_display = (
      'roll_no',
      'reg_no',
      'name',
      'standing_arrears',
      'history_of_arrears',
      'aggregate',
   )
   list_filter = (
      'batch',
      'standing_arrears'
   )
   inlines = [StudentSubjectInline,] # Leads to very long render time because all subjects are populated in about 58(number of course papers) dropdowns
   search_fields = ['roll_no','reg_no','name']

class FacultyAdmin(admin.ModelAdmin):
   list_display = (
      'fac_id',
      'name',
      'department'
   )
   search_fields = ['fac_id','name']

class BatchAdmin(admin.ModelAdmin):
   ordering = ('-year_of_graduation','section')
   list_display = (
      'course',
      'year_of_graduation',
      'section',
   )

class CourseAdmin(admin.ModelAdmin):
   ordering = ('-regulation','degree', 'department')
   list_display = (
      'degree',
      'department',
      'regulation'
   )

class SubjectInline(admin.TabularInline):
   model = Subject

class PaperAdmin(admin.ModelAdmin):
   ordering = ('-course__regulation', 'course__degree', 'course__department', 'during_sem', 'code')
   list_display = (
      'code',
      'name',
      'course',
      'during_sem'
   )
   inlines = [SubjectInline,]
   search_fields = ['code','name']

class SubjectAdmin(admin.ModelAdmin):
   ordering = ('paper','batch','lab_batch')
   list_display = (
      'paper',
      'batch',
      'lab_batch',
      'handled_by'
   )
   inlines = [StudentSubjectInline,]
   search_fields = ['paper__code','paper__name'] # Is necessary? May not scale for large data. All students are populated in about 60(a batch of students) dropdowns

class StudentSubjectAdmin(admin.ModelAdmin):
   ordering = ('student','subject')
   list_display = (
      'student',
      'subject',
      'internal_mark',
      'external_score'
   )

admin.site.register(Regulation)
admin.site.register(Department)
admin.site.register(Course, CourseAdmin)
admin.site.register(Paper, PaperAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(StudentSubject, StudentSubjectAdmin)
admin.site.register(ExternalScore)
