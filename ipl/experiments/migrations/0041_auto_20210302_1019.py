# Generated by Django 3.1.7 on 2021-03-02 09:19

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0040_auto_20210302_0653'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='microphone_check_page_tpl',
            field=tinymce.models.HTMLField(default='{% extends "experiments/base.html" %} {% load static %} {% block title %}Mikrofon einrichten{% endblock %} {% block content%}\n<div class="container" id="webcam-calibration" data-subject-uuid="{{ subject_data.id }}">\n    <div class="row">\n        <div class="col text-center">\n            <h1>Mikrofon einrichten</h1>\n        </div>\n    </div>\n    <div class="row">\n        <div class="col">\n            <div class="card active" id="webcam_step_2">\n                <div class="card-body">\n                    <p class="card-text">\n                        Für diese Studie ist es notwendig, dass Sie Zugriff auf Mikrofon erlauben.<br /><br />\n                        Ihr Browser wird Sie im nächsten Schritt um Erlaubnis bitten, Mikrofon freizuschalten. Klicken Sie dann bitte auf "Erlauben", um mit dem Experiment fortzufahren.<br /><br />\n                        Falls Ihnen die Option „immer erlauben“ angeboten wird, wählen Sie bitte diese, damit Ihr Browser die Einstellung speichert (nur für unseren Server). Sie können auch nur den Einzelfall erlauben. Dann wird Ihr Browser in den nächsten Schritten noch mehrmals um Erlaubnis zur Freischaltung von Mikrofon bitten.\n                    </p>\n                    <button type="button" class="btn btn-primary" disabled>Weiter</button>\n                </div>\n            </div>\n\n            <div class="card" id="webcam_step_4">\n                <div class="card-body">\n                    <p class="card-text">\n                        Unten sehen Sie das Probeaudio. Bitte spielen Sie dieses ab und beurteilen Sie, ob Ihr Kind und Sie gut sichtbar sind und ob der Ton aufgenommen wurde.<br /><br />\n                        Achten dabei bitte darauf, dass der Sound auf Ihrem Computer aktiviert ist.\n                    </p>\n                    <p class="card-text" id="upload-progress">\n                        <img src="{% static \'experiments/img/loading.gif\' %}" alt="Laden" title="Loading" />\n                    </p>\n                    <div class="alert alert-danger" role="alert" style="display: none;">\n                        Der Audio-Upload ist fehlgeschlagen.<br />\n                    </div>\n                    <div class="embed-responsive" style="display: none;">\n                    </div>\n                    <div class="alert alert-success" role="alert" style="display: none;">\n                        Der Audio-Upload war erfolgreich, bitte fahren Sie fort.\n                    </div>\n\n                    <button type="button" class="btn btn-primary" disabled data-target="{% url \'experiments:experimentRun\' subject_data.pk %}">Weiter (Ton haben funktioniert)</button>\n                    <button type="button" class="btn btn-warning" disabled data-toggle="modal" data-target="#repeatWebcamModal">Test Wiederholen (Es gab Probleme bei der Probeaufnahme)</button>\n                </div>\n            </div>\n\n        </div>\n    </div>\n</div>\n\n<div class="modal fade" id="repeatWebcamModal" tabindex="-1" role="dialog" aria-labelledby="repeatWebcamModalLabel" aria-hidden="true">\n    <div class="modal-dialog" role="document">\n        <div class="modal-content">\n            <div class="modal-header">\n                <h5 class="modal-title" id="repeatWebcamModalLabel">Mikrofon-Test Wiederholen</h5>\n                <button type="button" class="close" data-dismiss="modal" aria-label="Close">\n                    <span aria-hidden="true">&times;</span>\n                </button>\n            </div>\n            <div class="modal-body">\n                Falls Sie keinen Ton hören konnten: Stellen Sie bitte in den Soundeinstellungen Ihres Computers sicher, dass Ihr  und Ihr Lautsprecher aktiviert sind und überprüfen Sie, dass Ihr Ton nicht zu leise gestellt ist.\n            </div>\n            <div class="modal-footer">\n                <button type="button" class="btn btn-secondary" data-dismiss="modal">Abbrechen</button>\n                <button type="button" class="btn btn-primary" id="repeatRutton">Test Wiederholen</button>\n            </div>\n        </div>\n    </div>\n</div>\n\n<button id="exit-button" type="button" class="btn btn-secondary btn-sm">Beenden</button>\n<script>\n    var webcam_not_found = `Leider konnte Ihr Microfon nicht gefunden werden.<br /><br />Bitte stellen Sie sicher, dass ein Microfon angeschlossen ist und klicken Sie „Prüfung wiederholen“ um zum Mikrofon-Test zurückzukehren.<br /><br />Sollten Sie mit der Freischaltung Ihres Mikrofons nicht einverstanden sein und deshalb auf „nicht erlauben“ ausgewählt haben, schließen Sie bitte das Browser-Fenster.`;\n    var include_pause_page = "{{ experiment.include_pause_page }}";\n    var recording_option = "{{ experiment.recording_option }}";\n</script>\n<script src="{% static \'experiments/js/detectrtc.min.js\' %}"></script>\n<script src="{% static \'experiments/js/webcam-calibration.js\' %}"></script>\n{% endblock %}', verbose_name='Microphone check page template'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='webcam_check_page_tpl',
            field=tinymce.models.HTMLField(default='{% extends "experiments/base.html" %} {% load static %} {% block title %}Webcam und Mikrofon einrichten{% endblock %} {% block content%}\n<div class="container" id="webcam-calibration" data-subject-uuid="{{ subject_data.id }}">\n    <div class="row">\n        <div class="col text-center">\n            <h1>Webcam und Mikrofon einrichten</h1>\n        </div>\n    </div>\n    <div class="row">\n        <div class="col">\n            <div class="card active" id="webcam_step_2">\n                <div class="card-body">\n                    <p class="card-text">\n                        Für diese Studie ist es notwendig, dass Sie Zugriff auf Webcam und Mikrofon erlauben.<br /><br />\n                        Ihr Browser wird Sie im nächsten Schritt um Erlaubnis bitten, Webcam und Mikrofon freizuschalten. Klicken Sie dann bitte auf "Erlauben", um mit dem Experiment fortzufahren.<br /><br />\n                        Falls Ihnen die Option „immer erlauben“ angeboten wird, wählen Sie bitte diese, damit Ihr Browser die Einstellung speichert (nur für unseren Server). Sie können auch nur den Einzelfall erlauben. Dann wird Ihr Browser in den nächsten Schritten noch mehrmals um Erlaubnis zur Freischaltung von Webcam und Mikrofon bitten.\n                    </p>\n                    <button type="button" class="btn btn-primary" disabled>Weiter</button>\n                </div>\n            </div>\n\n            <div class="card" id="webcam_step_3">\n                <div class="card-body">\n                    <p class="card-text">\n                        Sie sehen nun unten ein Fenster mit dem Kamerabild. Bitte justieren Sie Ihre Kamera so, dass Ihr Kind gut sichtbar ist.<br /><br />\n                        Gleich machen wir eine kurze Probeaufnahme (ca. 3 Sekunden) um zu testen, ob die Aufnahme mit Bild und Ton funktioniert. Sobald sie unten klicken, startet die Probeaufnahme. Bitte sagen Sie nachdem Sie geklickt haben laut etwas (z.B. „hallo“), damit Sie die Tonaufnahme überprüfen können.\n                    </p>\n                    <div class="alert alert-danger" role="alert" style="display: none;"></div>\n                    <div class="embed-responsive" style="display: none;">\n                        <video controls class="embed-responsive-item"></video>\n                    </div>\n                    <button type="button" class="btn btn-primary" disabled>Probeaufnahme jetzt starten</button>\n                    <button type="button" class="btn btn-warning" id="repeat-check-button" style="display: none;">Webcam-Test wiederholen</button>\n                </div>\n            </div>\n\n            <div class="card" id="webcam_step_4">\n                <div class="card-body">\n                    <p class="card-text">\n                        Unten sehen Sie das Probevideo. Bitte spielen Sie dieses ab und beurteilen Sie, ob Ihr Kind und Sie gut sichtbar sind und ob der Ton aufgenommen wurde.<br /><br />\n                        Achten dabei bitte darauf, dass der Sound auf Ihrem Computer aktiviert ist.\n                    </p>\n                    <p class="card-text" id="upload-progress">\n                        <img src="{% static \'experiments/img/loading.gif\' %}" alt="Laden" title="Loading" />\n                    </p>\n                    <div class="alert alert-danger" role="alert" style="display: none;">\n                        Der Upload des Videos ist fehlgeschlagen.<br />\n                    </div>\n                    <div class="embed-responsive" style="display: none;">\n                    </div>\n                    <div class="alert alert-success" role="alert" style="display: none;">\n                        Der Upload des Videos war erfolgreich, bitte fahren Sie fort.\n                    </div>\n\n                    <button type="button" class="btn btn-primary" disabled data-target="{% url \'experiments:experimentRun\' subject_data.pk %}">Weiter (Bild und Ton haben funktioniert)</button>\n                    <button type="button" class="btn btn-warning" disabled data-toggle="modal" data-target="#repeatWebcamModal">Test Wiederholen (Es gab Probleme bei der Probeaufnahme)</button>\n                </div>\n            </div>\n\n        </div>\n    </div>\n</div>\n\n<div class="modal fade" id="repeatWebcamModal" tabindex="-1" role="dialog" aria-labelledby="repeatWebcamModalLabel" aria-hidden="true">\n    <div class="modal-dialog" role="document">\n        <div class="modal-content">\n            <div class="modal-header">\n                <h5 class="modal-title" id="repeatWebcamModalLabel">Webcam Test Wiederholen</h5>\n                <button type="button" class="close" data-dismiss="modal" aria-label="Close">\n                    <span aria-hidden="true">&times;</span>\n                </button>\n            </div>\n            <div class="modal-body">\n                Falls Sie keinen Ton hören konnten: Stellen Sie bitte in den Soundeinstellungen Ihres Computers sicher, dass Ihr  und Ihr Lautsprecher aktiviert sind und überprüfen Sie, dass Ihr Ton nicht zu leise gestellt ist.\n            </div>\n            <div class="modal-footer">\n                <button type="button" class="btn btn-secondary" data-dismiss="modal">Abbrechen</button>\n                <button type="button" class="btn btn-primary" id="repeatRutton">Test Wiederholen</button>\n            </div>\n        </div>\n    </div>\n</div>\n\n<button id="exit-button" type="button" class="btn btn-secondary btn-sm">Beenden</button>\n<script>\n    var webcam_not_found = `Leider konnte Ihre Webcam nicht gefunden werden.<br /><br />Bitte stellen Sie sicher, dass eine Webcam angeschlossen ist und klicken Sie „Prüfung wiederholen“ um zum Webcam-Test zurückzukehren.<br /><br />Sollten Sie mit der Freischaltung Ihrer Webcam nicht einverstanden sein und deshalb auf „nicht erlauben“ ausgewählt haben, schließen Sie bitte das Browser-Fenster.`;\n    var include_pause_page = "{{ experiment.include_pause_page }}";\n    var recording_option = "{{ experiment.recording_option }}";\n</script>\n<script src="{% static \'experiments/js/detectrtc.min.js\' %}"></script>\n<script src="{% static \'experiments/js/webcam-calibration.js\' %}"></script>\n{% endblock %}', verbose_name='Webcam check page template'),
        ),
    ]