# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Regulation'
        db.create_table('academics_regulation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year_formed', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('scoring_system', self.gf('django.db.models.fields.CharField')(default='G', max_length=1)),
        ))
        db.send_create_signal('academics', ['Regulation'])

        # Adding model 'Department'
        db.create_table('academics_department', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('abbr', self.gf('django.db.models.fields.CharField')(unique=True, max_length=4)),
        ))
        db.send_create_signal('academics', ['Department'])

        # Adding model 'Course'
        db.create_table('academics_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('degree', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academics.Department'])),
            ('regulation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academics.Regulation'])),
        ))
        db.send_create_signal('academics', ['Course'])

        # Adding unique constraint on 'Course', fields ['degree', 'department', 'regulation']
        db.create_unique('academics_course', ['degree', 'department_id', 'regulation_id'])

        # Adding model 'Faculty'
        db.create_table('academics_faculty', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academics.Department'])),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('phone_no', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('email_id', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('designation', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('date_of_joining', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('salary', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('qualification', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('experience', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('academics', ['Faculty'])

        # Adding model 'Paper'
        db.create_table('academics_paper', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academics.Course'])),
            ('during_sem', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('credits', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('academics', ['Paper'])

        # Adding unique constraint on 'Paper', fields ['code', 'course']
        db.create_unique('academics_paper', ['code', 'course_id'])

        # Adding model 'Batch'
        db.create_table('academics_batch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academics.Course'])),
            ('year_of_graduation', self.gf('django.db.models.fields.IntegerField')()),
            ('section', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('class_teacher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academics.Faculty'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('academics', ['Batch'])

        # Adding unique constraint on 'Batch', fields ['course', 'year_of_graduation', 'section']
        db.create_unique('academics_batch', ['course_id', 'year_of_graduation', 'section'])

        # Adding model 'Subject'
        db.create_table('academics_subject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('paper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academics.Paper'], null=True, blank=True)),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academics.Batch'])),
            ('handled_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academics.Faculty'], null=True, blank=True)),
        ))
        db.send_create_signal('academics', ['Subject'])

        # Adding unique constraint on 'Subject', fields ['paper', 'batch']
        db.create_unique('academics_subject', ['paper_id', 'batch_id'])

        # Adding model 'Student'
        db.create_table('academics_student', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('admission', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('staying', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('phone_no', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('email_id', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('roll_no', self.gf('django.db.models.fields.CharField')(unique=True, max_length=8)),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academics.Batch'])),
            ('college_status', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('reg_no', self.gf('django.db.models.fields.CharField')(max_length=11, null=True, blank=True)),
            ('university_status', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('aggregate', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('standing_arrears', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('history_of_arrears', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('academics', ['Student'])

        # Adding model 'AssessmentMark'
        db.create_table('academics_assessmentmark', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assessment_marks', to=orm['academics.Student'])),
            ('paper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academics.Paper'])),
            ('internal_mark', self.gf('django.db.models.fields.IntegerField')()),
            ('external_mark', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('external_grade', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('isPassed', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('attempt', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('latest_attempt', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('academics', ['AssessmentMark'])


    def backwards(self, orm):
        
        # Deleting model 'Regulation'
        db.delete_table('academics_regulation')

        # Deleting model 'Department'
        db.delete_table('academics_department')

        # Deleting model 'Course'
        db.delete_table('academics_course')

        # Removing unique constraint on 'Course', fields ['degree', 'department', 'regulation']
        db.delete_unique('academics_course', ['degree', 'department_id', 'regulation_id'])

        # Deleting model 'Faculty'
        db.delete_table('academics_faculty')

        # Deleting model 'Paper'
        db.delete_table('academics_paper')

        # Removing unique constraint on 'Paper', fields ['code', 'course']
        db.delete_unique('academics_paper', ['code', 'course_id'])

        # Deleting model 'Batch'
        db.delete_table('academics_batch')

        # Removing unique constraint on 'Batch', fields ['course', 'year_of_graduation', 'section']
        db.delete_unique('academics_batch', ['course_id', 'year_of_graduation', 'section'])

        # Deleting model 'Subject'
        db.delete_table('academics_subject')

        # Removing unique constraint on 'Subject', fields ['paper', 'batch']
        db.delete_unique('academics_subject', ['paper_id', 'batch_id'])

        # Deleting model 'Student'
        db.delete_table('academics_student')

        # Deleting model 'AssessmentMark'
        db.delete_table('academics_assessmentmark')


    models = {
        'academics.assessmentmark': {
            'Meta': {'object_name': 'AssessmentMark'},
            'attempt': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'external_grade': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'external_mark': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_mark': ('django.db.models.fields.IntegerField', [], {}),
            'isPassed': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'latest_attempt': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academics.Paper']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assessment_marks'", 'to': "orm['academics.Student']"})
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
