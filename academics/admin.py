from models import Student,Faculty,Department,Batch,Subject,AssessmentMark, Regulation, Paper, Course
from django.contrib import admin

class AssessmentMarkInline(admin.TabularInline):
   model = AssessmentMark

class StudentAdmin(admin.ModelAdmin):
   inlines = [AssessmentMarkInline,]
   list_display = (
      'roll_no',
      'reg_no',
      'name',
      'standing_arrears',
      'history_of_arrears',
      'aggregate',
   )
class PaperAdmin(admin.ModelAdmin):
   inlines = [AssessmentMarkInline,]

class StudentInline(admin.TabularInline):
   model = Student

class SubjectInline(admin.TabularInline):
   model = Subject

class BatchAdmin(admin.ModelAdmin):
   inlines = [
      StudentInline,
      SubjectInline,
   ]
admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Batch, BatchAdmin)
admin.site.register(Subject)
admin.site.register(AssessmentMark)
admin.site.register(Regulation)
admin.site.register(Paper, PaperAdmin)
admin.site.register(Course)

