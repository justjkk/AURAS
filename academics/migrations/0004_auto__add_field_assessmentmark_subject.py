# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'AssessmentMark.subject'
        db.add_column('academics_assessmentmark', 'subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academics.Subject'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'AssessmentMark.subject'
        db.delete_column('academics_assessmentmark', 'subject_id')


    models = {
        'academics.assessmentmark': {
            'Meta': {'object_name': 'AssessmentMark'},
            'academic_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'attempt': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'external_grade': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'external_mark': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_mark': ('django.db.models.fields.IntegerField', [], {}),
            'isPassed': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'latest_attempt': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academics.Paper']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assessment_marks'", 'to': "orm['academics.Student']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academics.Subject']", 'null': 'True', 'blank': 'True'})
        },
        'academics.batch': {
            'Meta': {'unique_together': "(['course', 'year_of_graduation', 'section'],)", 'object_name': 'Batch'},
            'class_teacher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academics.Faculty']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academics.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'year_of_graduation': ('django.db.models.fields.IntegerField', [], {})
        },
        'academics.course': {
            'Meta': {'unique_together': "(['degree', 'department', 'regulation'],)", 'object_name': 'Course'},
            'degree': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academics.Department']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_of_semesters': ('django.db.models.fields.IntegerField', [], {'default': '8'}),
            'regulation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academics.Regulation']"})
        },
        'academics.department': {
            'Meta': {'object_name': 'Department'},
            'abbr': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'academics.faculty': {
            'Meta': {'object_name': 'Faculty'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'date_of_joining': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academics.Department']"}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'email_id': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'experience': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'qualification': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'salary': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'academics.paper': {
            'Meta': {'unique_together': "(['code', 'course'],)", 'object_name': 'Paper'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academics.Course']"}),
            'credits': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'during_sem': ('django.db.models.fields.SmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'academics.regulation': {
            'Meta': {'object_name': 'Regulation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scoring_system': ('django.db.models.fields.CharField', [], {'default': "'G'", 'max_length': '1'}),
            'year_formed': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        },
        'academics.student': {
            'Meta': {'object_name': 'Student'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'admission': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'aggregate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academics.Batch']"}),
            'college_status': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'email_id': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'history_of_arrears': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'reg_no': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'roll_no': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'standing_arrears': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'staying': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'university_status': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'academics.subject': {
            'Meta': {'unique_together': "(['paper', 'batch'],)", 'object_name': 'Subject'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academics.Batch']"}),
            'handled_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academics.Faculty']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academics.Paper']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['academics']
