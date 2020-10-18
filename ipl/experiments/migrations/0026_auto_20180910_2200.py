# Generated by Django 2.0.8 on 2018-09-10 20:00

from django.db import migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0025_auto_20180909_2155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiment',
            name='alt_thank_you',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='alt_thank_you_title',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='browser_check',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='browser_check_title',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='consent_fail_reason',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='consent_fail_title',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='demographic_data',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='demographic_data_title',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='fullscreen_message',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='introduction',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='introduction_title',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='pause_page',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='pause_page_title',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='thank_you',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='thank_you_title',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='webcam_check_1',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='webcam_check_2',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='webcam_check_3',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='webcam_check_3_repeat',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='webcam_check_title',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='webcam_not_found',
        ),
        migrations.AddField(
            model_name='experiment',
            name='browser_check_page_tpl',
            field=filebrowser.fields.FileBrowseField(default='uploads/templates/browsercheck_de.html', max_length=250, verbose_name='browser check page template'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='consent_fail_page_tpl',
            field=filebrowser.fields.FileBrowseField(default='uploads/templates/fail_de.html', max_length=250, verbose_name='consent failed page template'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='demographic_data_page_tpl',
            field=filebrowser.fields.FileBrowseField(default='uploads/templates/subjectForm_de.html', max_length=250, verbose_name='demographic data page template'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='error_page_tpl',
            field=filebrowser.fields.FileBrowseField(default='uploads/templates/error_de.html', max_length=250, verbose_name='error page template'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='experiment_page_tpl',
            field=filebrowser.fields.FileBrowseField(default='uploads/templates/experiment_de.html', max_length=250, verbose_name='experiment page template'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='introduction_page_tpl',
            field=filebrowser.fields.FileBrowseField(default='uploads/templates/consentForm_de.html', max_length=250, verbose_name='consent form template'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='pause_page_tpl',
            field=filebrowser.fields.FileBrowseField(default='uploads/templates/pause_de.html', max_length=250, verbose_name='pause page template'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='thank_you_abort_page_tpl',
            field=filebrowser.fields.FileBrowseField(default='uploads/templates/alternatethankyou_de.html', max_length=250, verbose_name='end page after discontinuation template'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='thank_you_page_tpl',
            field=filebrowser.fields.FileBrowseField(default='uploads/templates/thankyou_de.html', max_length=250, verbose_name='standard end page template'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='webcam_check_page_tpl',
            field=filebrowser.fields.FileBrowseField(default='uploads/templates/webcamTest_de.html', max_length=250, verbose_name='webcam check page template'),
        ),
    ]