import reporting
from django.db.models import Sum, Avg, Count
from models import Student,Faculty,Batch,Department

class StudentReport(reporting.Report):
    model = Student
    verbose_name = 'Student Report'
    annotate = (                    # Annotation fields (tupples of field, func, title)
        ('id', Count, 'Total'),     # example of custom title for column 
    )
    aggregate = (                   # columns that will be aggregated (syntax the same as for annotate)
        ('id', Count, 'Total'),
    )
    group_by = [                   # list of fields and lookups for group-by options
        'batch__course__department',
        'batch',
    ]
    list_filter = [                # This are report filter options (similar to django-admin)
        'gender',
        'staying',
        'admission',
        'batch__course__department__abbr',
        'batch',
        'standing_arrears',
    ]
    
    detail_list_display = [        # if detail_list_display is defined user will be able to see how rows was grouped  
        'name', 
        'roll_no',
        'phone_no',
        'email_id',
    ]

class FacultyReport(reporting.Report):
    model = Faculty
    verbose_name = 'Faculty Report'
    annotate = (                    # Annotation fields (tupples of field, func, title)
        ('id', Count, 'Total'),     # example of custom title for column 
    )
    aggregate = (                   # columns that will be aggregated (syntax the same as for annotate)
        ('id', Count, 'Total'),
    )
    group_by = [                   # list of fields and lookups for group-by options
        'department',
        'designation',
    ]
    list_filter = [                # This are report filter options (similar to django-admin)
        'department',
        'designation',
    ]
    
    detail_list_display = [        # if detail_list_display is defined user will be able to see how rows was grouped  
        'name', 
        'phone_no',
        'email_id',
        'department',
        'designation',
    ]

reporting.register('student', StudentReport) # Do not forget to 'register' your class in reports
reporting.register('faculty', FacultyReport) # Do not forget to 'register' your class in reports
