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
            ('number_of_semesters', self.gf('django.db.models.fields.IntegerField')(default=8)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(related_name='courses', to=orm['academics.Department'])),
            ('regulation', self.gf('django.db.models.fields.related.ForeignKey')(related_name='courses', to=orm['academics.Regulation'])),
        ))
        db.send_create_signal('academics', ['Course'])

        # Adding unique constraint on 'Course', fields ['degree', 'department', 'regulation']
        db.create_unique('academics_course', ['degree', 'department_id', 'regulation_id'])

        # Adding model 'Faculty'
        db.create_table('academics_faculty', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fac_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(related_name='faculties', to=orm['academics.Department'])),
        ))
        db.send_create_signal('academics', ['Faculty'])

        # Adding model 'Paper'
        db.create_table('academics_paper', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='papers', to=orm['academics.Course'])),
            ('during_sem', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('credits', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('is_lab_paper', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('academics', ['Paper'])

        # Adding unique constraint on 'Paper', fields ['code', 'course']
        db.create_unique('academics_paper', ['code', 'course_id'])

        # Adding model 'Batch'
        db.create_table('academics_batch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='batches', to=orm['academics.Course'])),
            ('year_of_graduation', self.gf('django.db.models.fields.IntegerField')()),
            ('section', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('academics', ['Batch'])

        # Adding unique constraint on 'Batch', fields ['course', 'year_of_graduation', 'section']
        db.create_unique('academics_batch', ['course_id', 'year_of_graduation', 'section'])

        # Adding model 'Subject'
        db.create_table('academics_subject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('paper', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subjects', to=orm['academics.Paper'])),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subjects', to=orm['academics.Batch'])),
            ('handled_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='subjects_handled', null=True, to=orm['academics.Faculty'])),
            ('hours_spent', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('lab_batch', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('academics', ['Subject'])

        # Adding unique constraint on 'Subject', fields ['paper', 'batch', 'lab_batch']
        db.create_unique('academics_subject', ['paper_id', 'batch_id', 'lab_batch'])

        # Adding model 'Student'
        db.create_table('academics_student', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('admission', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('staying', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('roll_no', self.gf('django.db.models.fields.CharField')(unique=True, max_length=8)),
            ('reg_no', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(related_name='students', to=orm['academics.Batch'])),
            ('lab_batch', self.gf('django.db.models.fields.IntegerField')()),
            ('aggregate', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('standing_arrears', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('history_of_arrears', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('academics', ['Student'])

        # Adding model 'StudentSubject'
        db.create_table('academics_studentsubject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academics.Student'])),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academics.Subject'])),
            ('internal_mark', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('external_score', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academics.ExternalScore'], null=True, blank=True)),
            ('hours_attended', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('is_passed', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('number_of_attempts', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('academics', ['StudentSubject'])

        # Adding model 'ExternalScore'
        db.create_table('academics_externalscore', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student_subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='external_scores', to=orm['academics.StudentSubject'])),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
            ('is_passed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('attempt', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('academics', ['ExternalScore'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Subject', fields ['paper', 'batch', 'lab_batch']
        db.delete_unique('academics_subject', ['paper_id', 'batch_id', 'lab_batch'])

        # Removing unique constraint on 'Batch', fields ['course', 'year_of_graduation', 'section']
        db.delete_unique('academics_batch', ['course_id', 'year_of_graduation', 'section'])

        # Removing unique constraint on 'Paper', fields ['code', 'course']
        db.delete_unique('academics_paper', ['code', 'course_id'])

        # Removing unique constraint on 'Course', fields ['degree', 'department', 'regulation']
        db.delete_unique('academics_course', ['degree', 'department_id', 'regulation_id'])

        # Deleting model 'Regulation'
        db.delete_table('academics_regulation')

        # Deleting model 'Department'
        db.delete_table('academics_department')

        # Deleting model 'Course'
        db.delete_table('academics_course')

        # Deleting model 'Faculty'
        db.delete_table('academics_faculty')

        # Deleting model 'Paper'
        db.delete_table('academics_paper')

        # Deleting model 'Batch'
        db.delete_table('academics_batch')

        # Deleting model 'Subject'
        db.delete_table('academics_subject')

        # Deleting model 'Student'
        db.delete_table('academics_student')

        # Deleting model 'StudentSubject'
        db.delete_table('academics_studentsubject')

        # Deleting model 'ExternalScore'
        db.delete_table('academics_externalscore')


    models = {
        'academics.batch': {
            'Meta': {'unique_together': "(['course', 'year_of_graduation', 'section'],)", 'object_name': 'Batch'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'batches'", 'to': "orm['academics.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'year_of_graduation': ('django.db.models.fields.IntegerField', [], {})
        },
        'academics.course': {
            'Meta': {'unique_together': "(['degree', 'department', 'regulation'],)", 'object_name': 'Course'},
            'degree': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses'", 'to': "orm['academics.Department']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_of_semesters': ('django.db.models.fields.IntegerField', [], {'default': '8'}),
            'regulation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses'", 'to': "orm['academics.Regulation']"})
        },
        'academics.department': {
            'Meta': {'object_name': 'Department'},
            'abbr': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'academics.externalscore': {
            'Meta': {'object_name': 'ExternalScore'},
            'attempt': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_passed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'score': ('django.db.models.fields.IntegerField', [], {}),
            'student_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'external_scores'", 'to': "orm['academics.StudentSubject']"})
        },
        'academics.faculty': {
            'Meta': {'object_name': 'Faculty'},
            'department': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'faculties'", 'to': "orm['academics.Department']"}),
            'fac_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'academics.paper': {
            'Meta': {'unique_together': "(['code', 'course'],)", 'object_name': 'Paper'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'papers'", 'to': "orm['academics.Course']"}),
            'credits': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'during_sem': ('django.db.models.fields.SmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_lab_paper': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'academics.regulation': {
            'Meta': {'object_name': 'Regulation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scoring_system': ('django.db.models.fields.CharField', [], {'default': "'G'", 'max_length': '1'}),
            'year_formed': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        },
        'academics.student': {
            'Meta': {'ordering': "['roll_no']", 'object_name': 'Student'},
            'admission': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'aggregate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'students'", 'to': "orm['academics.Batch']"}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'history_of_arrears': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab_batch': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'reg_no': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'roll_no': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'standing_arrears': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'staying': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['academics.Subject']", 'through': "orm['academics.StudentSubject']", 'symmetrical': 'False'})
        },
        'academics.studentsubject': {
            'Meta': {'object_name': 'StudentSubject'},
            'external_score': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academics.ExternalScore']", 'null': 'True', 'blank': 'True'}),
            'hours_attended': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_mark': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_passed': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'number_of_attempts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academics.Student']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academics.Subject']"})
        },
        'academics.subject': {
            'Meta': {'ordering': "['paper__name']", 'unique_together': "(['paper', 'batch', 'lab_batch'],)", 'object_name': 'Subject'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subjects'", 'to': "orm['academics.Batch']"}),
            'handled_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subjects_handled'", 'null': 'True', 'to': "orm['academics.Faculty']"}),
            'hours_spent': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab_batch': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subjects'", 'to': "orm['academics.Paper']"})
        }
    }

    complete_apps = ['academics']
