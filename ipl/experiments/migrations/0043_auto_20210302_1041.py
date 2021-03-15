# Generated by Django 3.1.7 on 2021-03-02 09:41

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0042_auto_20210302_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='experiment_page_tpl',
            field=tinymce.models.HTMLField(default='{% extends "experiments/base.html" %} \n{% load static %}\n\n{% block title %}Experiment{% endblock %} \n\n{% block content %}\n<div class="container h-100 text-center" id="fullscreen-message">\n    <div class="row h-100 justify-content-center align-items-center">\n        <div class="col">\n            <p class="card-text">\n                Gleich geht es los!<br /><br />\n                Bevor die Studie startet, möchten wir noch eine kurze Erklärung von Ihnen aufzeichnen. Lesen Sie dafür bitte den Text auf der nächsten Seite mit Ihrem Kind auf dem Schoß laut vor. <br /><br />\n                Diese wiederholte Erklärung ist uns wichtig, da wir wirklich sichergehen möchten, dass Sie die Rahmenbedingungen verstanden haben und mit Ihnen einverstanden sind. Sollte uns diese Aufnahme nicht vorliegen, werden wir Ihre Daten und Videos löschen. <br /><br />\n                Nach der Erklärung startet die Studie direkt. Folgen Sie dann bitte den Hinweisen auf dem Monitor. <br />\n                Die Studie wird im Vollbild dargeboten. Sollten Sie die Studie zwischendurch beenden oder unterbrechen wollen, klicken Sie bitte unten rechts auf „beenden“. <br /><br />\n                Um fortzufahren, klicken Sie bitte „Vollbild aktivieren“\n            </p>\n            <button id="fullscreen-button" type="button" class="btn btn-primary">Vollbild aktivieren</button>\n        </div>\n    </div>\n</div>\n\n<button id="exit-button" type="button" class="btn btn-secondary btn-sm">Beenden</button>\n\n<div id="trials" style="display: none;" data-subject-uuid="{{ subject_data.id }}" data-subject-id="{{ subject_data.participant_id }}"></div>\n\n<script>\n    var trials = {{ trials|safe }}\n    var loading_image = "{{ loading_image.url }}";\n    var global_timeout = "{{ global_timeout }}";\n    var include_pause_page = "{{ include_pause_page }}";\n    var recording_option = "{{ recording_option }}";\n    var general_onset = "{{ general_onset }}";\n</script>\n \n<script src="{% static \'experiments/js/experiment.js\' %}"></script>\n{% endblock %}\n', verbose_name='experiment page template'),
        ),
    ]