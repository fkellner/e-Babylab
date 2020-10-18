from django.contrib import admin
from django import forms
from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth.models import Group
from django.core import serializers

from filebrowser.base import FileObject

from .models import Experiment, ListItem, OuterBlockItem, BlockItem, TrialItem, ConsentQuestion
from .models import Question, SubjectData, AnswerText, AnswerRadio, AnswerSelect, AnswerInteger, AnswerSelectMultiple, TrialResult
from .forms import ExperimentForm

from django.utils.html import format_html
from django.urls import reverse
from django.forms import Textarea
from django.db import models
from django.db.models import Q

import os
import uuid
from datetime import datetime
import json


class TrialItemInline(admin.StackedInline):
    model = TrialItem
    extra = 0
    verbose_name = "Trial"
    verbose_name_plural = "Trials"
    inline_classes = ['grp-collapse grp-open']
    sortable_field_name = "position"


class BlockItemInline(admin.StackedInline):
    model = BlockItem
    extra = 0
    show_change_link = True
    verbose_name = "Inner block"
    verbose_name_plural = "Inner blocks"
    inline_classes = ['grp-collapse grp-open']
    sortable_field_name = "position"


class OuterBlockItemInline(admin.StackedInline):
    model = OuterBlockItem
    extra = 0
    show_change_link = True
    verbose_name = "Outer block"
    verbose_name_plural = "Outer blocks"
    inline_classes = ['grp-collapse grp-open']
    sortable_field_name = "position"


class ListItemInline(admin.StackedInline):
    model = ListItem
    extra = 0
    show_change_link = True
    verbose_name = "List"
    verbose_name_plural = "Lists"
    inline_classes = ['grp-collapse grp-open']


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0
    verbose_name = "Field"
    verbose_name_plural = "Demographic information"
    classes = ['grp-collapse grp-closed']
    inline_classes = ['grp-collapse grp-open']
    sortable_field_name = "position"
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={
                'rows': 3,
                'cols': 85
            })
        },
    }


class AnswerBaseInline(admin.StackedInline):
    fields = ('question', 'body')
    readonly_fields = ('question', 'body')
    extra = 0
    inline_classes = ['grp-collapse grp-open']

    def has_add_permission(self, request, obj=None):
        """
        Disables adding of Answers as they should only be created during an experiment.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Disallow deleting of an Answer
        """
        return False


class AnswerTextInline(AnswerBaseInline):
    model = AnswerText


class AnswerRadioInline(AnswerBaseInline):
    model = AnswerRadio


class AnswerSelectInline(AnswerBaseInline):
    model = AnswerSelect


class AnswerSelectMultipleInline(AnswerBaseInline):
    model = AnswerSelectMultiple


class AnswerIntegerInline(AnswerBaseInline):
    model = AnswerInteger


class ConsentQuestionInline(admin.StackedInline):
    model = ConsentQuestion
    extra = 0
    classes = ['grp-collapse grp-closed']
    inline_classes = ['grp-collapse grp-open']
    sortable_field_name = "position"
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={
                'rows': 3,
                'cols': 85
            })
        },
    }


class ExperimentAdmin(admin.ModelAdmin):
    form = ExperimentForm
    fieldsets = [
        (None, {
            'fields': (
                'exp_name',
                'created_on',
                'sharing_option',
                'sharing_groups',
                'list_selection_strategy',
                'recording_option',
                'loading_image',
                'include_pause_page',
            )
        }),
        ('Templates', {
            'classes': ('grp-collapse grp-closed', ),
            'fields': (
                'information_page_tpl', 
                'browser_check_page_tpl',
                'introduction_page_tpl',
                'consent_fail_page_tpl',
                'demographic_data_page_tpl',
                'webcam_check_page_tpl',
                'experiment_page_tpl',
                'pause_page_tpl',
                'thank_you_page_tpl',
                'thank_you_abort_page_tpl',
                'error_page_tpl',
            ),
        })
    ]
    inlines = [ConsentQuestionInline, QuestionInline, ListItemInline]
    list_display = ('exp_name', 'created_on', 'experiment_buttons')
    list_filter = ['created_on']
    search_fields = ['exp_name']
    change_list_filter_template = "admin/filter_listing.html"
     
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        """
        Returns a QuerySet of experiments which the user has access to.
        """
        qs = super(ExperimentAdmin, self).get_queryset(request)
        user_groups = request.user.groups.values_list('id', flat=True)
        user_owned = Q(user=request.user)
        shared_to_group = Q(sharing_option='GRP')
        shared_to_user_groups = Q(sharing_groups__in=user_groups)
        shared_to_everyone = Q(sharing_option='PUB')

        if request.user.is_superuser:
            return qs
        elif request.user.groups.exists():  # user belongs to group(s)
            return qs.filter(user_owned | shared_to_everyone
                             | shared_to_group & shared_to_user_groups)
        else:
            return qs.filter(user_owned | shared_to_everyone)

    def has_change_permission(self, request, obj=None):
        """
        Checks if user has permission to change an experiment.
        """
        user_groups = request.user.groups.values_list('id')
        if not obj:
            return True
        elif obj.sharing_option == 'PUB' or obj.sharing_option == 'GRP' and user_groups.intersection(
                obj.sharing_groups.values_list('id')):
            return True
        else:
            return obj.user == request.user or request.user.is_superuser

    def experiment_buttons(self, obj):
        """
        Displays action buttons for the Experiment admin interface.
        """
        return format_html(
            '<a class="grp-button" href="{url_exp}">Go to Experiment</a>&nbsp;'
            + '<a class="grp-button" href="{url_report}">Download Results</a>&nbsp;'
            + '<a class="grp-button" href="{url_export}">Export Experiment</a>',
            url_exp=reverse('experiments:informationPage', args=[obj.id]),
            url_report=reverse('experiments:experimentReport', args=[obj.id]),
            url_export=reverse('experiments:experimentExport', args=[obj.id]))

    experiment_buttons.allow_tags = True
    experiment_buttons.short_description = 'Actions'

    @staticmethod
    def exportToJSON(experiment_id):
        """
        Creates a JSON object of the experiment to be exported.
        """

        # Get all data
        experiment = Experiment.objects.filter(pk=experiment_id)
        lists = ListItem.objects.filter(experiment=experiment_id)
        outerblocks = OuterBlockItem.objects.filter(listitem__experiment=experiment_id)
        innerblocks = BlockItem.objects.filter(outerblockitem__listitem__experiment=experiment_id)
        trials = TrialItem.objects.filter(blockitem__outerblockitem__listitem__experiment=experiment_id)
        questions = Question.objects.filter(experiment=experiment_id)
        consentquestions = ConsentQuestion.objects.filter(experiment=experiment_id)

        # Serialize into JSON object
        json_data = {}
        json_data['experiment'] = json.loads(serializers.serialize("json", experiment))
        json_data['lists'] = json.loads(serializers.serialize("json", lists))
        json_data['outerblocks'] = json.loads(serializers.serialize("json", outerblocks))
        json_data['innerblocks'] = json.loads(serializers.serialize("json", innerblocks))
        json_data['trials'] = json.loads(serializers.serialize("json", trials))
        json_data['questions'] = json.loads(serializers.serialize("json", questions))
        json_data['consentquestions'] = json.loads(serializers.serialize("json", consentquestions))

        return json_data

    @staticmethod
    def importFromJSON(request, data):
        """
        Imports an experiment from JSON file data.
        """

        json_data = data.decode("utf-8")

        # Import experiment
        for experiment in serializers.deserialize("json", json.dumps(json.loads(json_data)['experiment'])):
            old_primary_key = str(experiment.object.id)

            experiment.object.created_on = datetime.now()
            experiment.object.user = request.user
            experiment.object.id = None 

            # Save as new experiment
            experiment.save()
            new_primary_key = str(experiment.object.id)

            # Replace all experiment ids
            json_data = json_data.replace(old_primary_key, new_primary_key)

        # Import lists
        for listItem in serializers.deserialize("json", json.dumps(json.loads(json_data)['lists'])):
            old_primary_key = str(listItem.object.id)

            listItem.object.id = None 

            # Save as new list
            listItem.save()
            new_primary_key = str(listItem.object.id)

            # Replace all list ids
            json_data = json_data.replace('"listitem": {},'.format(old_primary_key), '"listitem": {},'.format(new_primary_key))

        # Import outer blocks
        for outerBlockItem in serializers.deserialize("json", json.dumps(json.loads(json_data)['outerblocks'])):
            old_primary_key = str(outerBlockItem.object.id)

            outerBlockItem.object.id = None 

            # Save as new outer block
            outerBlockItem.save()
            new_primary_key = str(outerBlockItem.object.id)

            # Replace all outer block ids
            json_data = json_data.replace('"outerblockitem": {},'.format(old_primary_key), '"outerblockitem": {},'.format(new_primary_key))

        # Import inner blocks
        for innerBlockItem in serializers.deserialize("json", json.dumps(json.loads(json_data)['innerblocks'])):
            old_primary_key = str(innerBlockItem.object.id)

            innerBlockItem.object.id = None 

            # Save as new inner block
            innerBlockItem.save()
            new_primary_key = str(innerBlockItem.object.id)

            # Replace all inner block ids
            json_data = json_data.replace('"blockitem": {},'.format(old_primary_key), '"blockitem": {},'.format(new_primary_key))

        # Import trials
        for trialItem in serializers.deserialize("json", json.dumps(json.loads(json_data)['trials'])):
            old_primary_key = str(trialItem.object.id)

            trialItem.object.id = None 

            # Save as new trial
            trialItem.save()
            new_primary_key = str(trialItem.object.id)

        # Import questions
        for question in serializers.deserialize("json", json.dumps(json.loads(json_data)['questions'])):
            old_primary_key = str(question.object.id)

            question.object.id = None 

            # Save as new question
            question.save()
            new_primary_key = str(question.object.id)

        # Import consent questions
        for consentQuestion in serializers.deserialize("json", json.dumps(json.loads(json_data)['consentquestions'])):
            old_primary_key = str(consentQuestion.object.id)

            consentQuestion.object.id = None 

            # Save as new consent question
            consentQuestion.save()
            new_primary_key = str(consentQuestion.object.id)


class ListItemAdmin(admin.ModelAdmin):
    inlines = [OuterBlockItemInline]
    classes = ['grp-collapse grp-open']
    list_display = ('list_name', 'experiment', )
   
    def get_model_perms(self, request):
        """
        Returns empty perms dict thus hiding the model from admin index.
        """
        return {}

    def get_queryset(self, request):
        """
        Returns a QuerySet of list items which the user has access to.
        """
        qs = super(ListItemAdmin, self).get_queryset(request)
        user_groups = request.user.groups.values_list('id', flat=True)
        user_owned = Q(experiment__user=request.user)
        shared_to_group = Q(experiment__sharing_option='GRP')
        shared_to_user_groups = Q(experiment__sharing_groups__in=user_groups)
        shared_to_everyone = Q(experiment__sharing_option='PUB')

        if request.user.is_superuser:
            return qs
        elif request.user.groups.exists():  # user belongs to group(s)
            return qs.filter(user_owned | shared_to_everyone
                             | shared_to_group & shared_to_user_groups)
        else:
            return qs.filter(user_owned | shared_to_everyone)


class OuterBlockItemAdmin(admin.ModelAdmin):
    inlines = [BlockItemInline]
    classes = ['grp-collapse grp-open']
    list_display = ('outer_block_name', 'listitem', 'get_experiment' )

    def get_experiment(self, obj):
        return obj.listitem.experiment
    get_experiment.admin_order_field  = 'listitem'  # allow column order sorting
    get_experiment.short_description = 'Experiment'  # rename column head

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

    def get_queryset(self, request):
        """
        Returns a QuerySet of outer block items which the user has access to.
        """
        qs = super(OuterBlockItemAdmin, self).get_queryset(request)
        user_groups = request.user.groups.values_list('id', flat=True)
        user_owned = Q(listitem__experiment__user=request.user)
        shared_to_group = Q(listitem__experiment__sharing_option='GRP')
        shared_to_user_groups = Q(
            listitem__experiment__sharing_groups__in=user_groups)
        shared_to_everyone = Q(listitem__experiment__sharing_option='PUB')

        if request.user.is_superuser:
            return qs
        elif request.user.groups.exists():  # user belongs to group(s)
            return qs.filter(user_owned
                             | shared_to_group & shared_to_user_groups
                             | shared_to_everyone)
        else:
            return qs.filter(user_owned | shared_to_everyone)


class BlockItemAdmin(admin.ModelAdmin):
    inlines = [TrialItemInline]
    list_display = ('label', 'outerblockitem', 'get_listitem', 'get_experiment' )

    def get_listitem(self, obj):
        """
        Gets the list item associated to the block item.
        """
        return obj.outerblockitem.listitem
    get_listitem.admin_order_field  = 'outerblockitem'  # allow column order sorting
    get_listitem.short_description = 'List item'  # rename column head
        
    def get_experiment(self, obj):
        """
        Gets the experiment associated to the block item.
        """
        return obj.outerblockitem.listitem.experiment
    get_experiment.admin_order_field  = 'outerblockitem__listitem'  # allow column order sorting
    get_experiment.short_description = 'Experiment'  # rename column head

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

    def get_queryset(self, request):
        """
        Returns a QuerySet of (inner) block items which the user has access to.
        """
        qs = super(BlockItemAdmin, self).get_queryset(request)
        user_groups = request.user.groups.values_list('id', flat=True)
        user_owned = Q(outerblockitem__listitem__experiment__user=request.user)
        shared_to_group = Q(outerblockitem__listitem__experiment__sharing_option='GRP')
        shared_to_user_groups = Q(
            outerblockitem__listitem__experiment__sharing_groups__in=user_groups)
        shared_to_everyone = Q(outerblockitem__listitem__experiment__sharing_option='PUB')

        if request.user.is_superuser:
            return qs
        elif request.user.groups.exists():  # user belongs to group(s)
            return qs.filter(user_owned
                             | shared_to_group & shared_to_user_groups
                             | shared_to_everyone)
        else:
            return qs.filter(user_owned | shared_to_everyone)


class SubjectDataAdmin(admin.ModelAdmin):
    list_display = ('participant_id', 'experiment', 'listitem', 'created')
    list_filter = ['experiment']
    inlines = [
        AnswerTextInline, AnswerRadioInline, AnswerSelectInline,
        AnswerSelectMultipleInline, AnswerIntegerInline
    ]
    # specifies the order as well as which fields to act on
    readonly_fields = ('id', 'participant_id', 'experiment', 'listitem',
                       'created', 'updated', 'resolution_w', 'resolution_h')
    ordering = (
        'experiment',
        'participant_id',
    )

    def get_queryset(self, request):
        """
        Returns a QuerySet of SubjectData which the user has access to.
        """
        qs = super(SubjectDataAdmin, self).get_queryset(request)
        user_groups = request.user.groups.values_list('id', flat=True)
        user_owned = Q(experiment__user=request.user)
        shared_to_group = Q(experiment__sharing_option='GRP')
        shared_to_user_groups = Q(experiment__sharing_groups__in=user_groups)
        shared_to_everyone = Q(experiment__sharing_option='PUB')

        if request.user.is_superuser:
            return qs
        elif request.user.groups.exists():  # user belongs to group(s)
            return qs.filter(user_owned
                             | shared_to_group & shared_to_user_groups
                             | shared_to_everyone)
        else:
            return qs.filter(user_owned | shared_to_everyone)

    def has_change_permission(self, request, obj=None):
        """
        Checks if user has permission to change subject data.
        """
        user_groups = request.user.groups.values_list('id')
        if not obj:
            return True
        elif obj.experiment.sharing_option == 'PUB' or obj.experiment.sharing_option == 'GRP' and user_groups.intersection(
                obj.experiment.sharing_groups.values_list('id')):
            return True
        else:
            return obj.experiment.user == request.user or request.user.is_superuser

    def has_add_permission(self, request, obj=None):
        """
        Disable adding of SubjectData on the admin site as this should only be created during an experiment. 
        """
        return False


class TrialResultAdmin(admin.ModelAdmin):
    """
    This is not being used.
    """
    list_display = ('subject', 'date', 'trialitem', )
    readonly_fields = ('subject', 'trialitem', 'date', 'start_time',
                       'end_time', 'key_pressed', 'webcam_file_link')

    def webcam_file_link(self, obj):
        if obj.webcam_file:
            webcam_url = settings.WEBCAM_URL
            return webcam_url + obj.filename 
        else:
            return "-"

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("webcam_file", )
        form = super(TrialResultAdmin, self).get_form(request, obj, **kwargs)
        return form

    webcam_file_link.allow_tags = True
    webcam_file_link.short_description = 'Webcam file'

    def get_queryset(self, request):
        qs = super(TrialResultAdmin, self).get_queryset(request)
        user_groups = request.user.groups.values_list('id', flat=True)
        user_owned = Q(subject__experiment__user=request.user)
        shared_to_group = Q(subject__experiment__sharing_option='GRP')
        shared_to_user_groups = Q(
            subject__experiment__sharing_groups__in=user_groups)
        shared_to_everyone = Q(subject__experiment__sharing_option='PUB')

        if request.user.is_superuser:
            return qs
        elif request.user.groups.exists():  # user belongs to group(s)
            return qs.filter(user_owned
                             | shared_to_group & shared_to_user_groups
                             | shared_to_everyone)
        else:
            return qs.filter(user_owned | shared_to_everyone)

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

    def has_change_permission(self, request, obj=None):
        user_groups = request.user.groups.values_list('id')
        if not obj:
            return True
        elif obj.subject.experiment.sharing_option == 'PUB' or obj.subject.experiment.sharing_option == 'GRP' and user_groups.intersection(
                obj.subject.experiment.sharing_groups.values_list('id')):
            return True
        else:
            return obj.subject.experiment.user == request.user or request.user.is_superuser

    def has_add_permission(self, request, obj=None):
        return False


# Register your models here.
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(ListItem, ListItemAdmin)
admin.site.register(OuterBlockItem, OuterBlockItemAdmin)
admin.site.register(BlockItem, BlockItemAdmin)
admin.site.register(SubjectData, SubjectDataAdmin)
#admin.site.register(TrialResult, TrialResultAdmin)