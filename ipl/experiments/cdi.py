from django.shortcuts import get_object_or_404, render
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.text import get_valid_filename
from django.template import Template, RequestContext

from filebrowser.fields import FileBrowseField
from scipy.stats import norm

from .models import SubjectData, CdiResult, Experiment, Instrument
from .forms import VocabularyChecklistForm

import csv
import logging
import simplejson as json
import numpy as np
import os.path
import pandas as pd
import re
import uuid
import numexpr
import tqdm
import catsim

from catsim.initialization import FixedPointInitializer
from catsim.selection import MaxInfoSelector
from catsim.estimation import HillClimbingEstimator
from catsim.stopping import MaxItemStopper
from catsim.irt import icc, max_info_hpc, inf_hpc


# Create a logger for this file
logger = logging.getLogger(__name__)

def sort_items(item_params):
    """
    Return ndarray of indices of items sorted by maximum item information.
    """
    return (-inf_hpc(max_info_hpc(item_params), item_params)).argsort()

def cdiRun(request, run_uuid):
    """
    Administer CDI-IRT
    """
    subject_data = get_object_or_404(SubjectData, pk=run_uuid)
    experiment = get_object_or_404(Experiment, pk=subject_data.experiment.pk)
    instrument = get_object_or_404(Instrument, pk=experiment.instrument.pk)

    try:
        # parse instrument word list
        all_words_reader = csv.DictReader(open(os.path.join(settings.MEDIA_ROOT, instrument.words_list.path), mode='r', encoding='utf-8-sig'), delimiter = ',')
        all_words = []
        for row in all_words_reader:
            all_words.append(row['word'])
        request.session['all_words'] = json.dumps(all_words)
        
        # get IRT parameters
        item_params = pd.read_csv(os.path.join(settings.MEDIA_ROOT, instrument.irt_params.path))
        item_params = item_params.iloc[:, 1:5]
        request.session['item_params'] = item_params.reset_index().to_json(orient='records')

        # administer first item
        administered_items = sort_items(item_params.to_numpy())[0:1, ].tolist()
        request.session['administered_items'] = administered_items
        irt_run = 0
        request.session['irt_run'] = irt_run
        request.session['est_theta'] = FixedPointInitializer(-5).initialize() # start low, assume all poor learners
        words = []
        words.append(all_words[administered_items[irt_run]])
        request.session['words'] = words
        request.session['responses'] = []
        
        form = VocabularyChecklistForm(cdi_form=experiment, word=words[irt_run])
    except KeyError as e:
        logger.exception('Failed to generate cdi item: ' + str(e))
        return HttpResponseRedirect(reverse('experiments:experimentError', args=(run_uuid,)))
    else:
        t = Template(experiment.cdi_page_tpl)
        c = RequestContext(request, {'subject_data': subject_data, 'cdi_form':form, 'experiment': experiment,})
        return HttpResponse(t.render(c))

def cdiSubmit(request, run_uuid):
    """
    Stores item response as CdiResult.
    """
    subject_data = get_object_or_404(SubjectData, pk=run_uuid)
    experiment = get_object_or_404(Experiment, pk=subject_data.experiment.pk)
    form = VocabularyChecklistForm(request.POST, cdi_form=experiment)
    
    # store current response as CdiResult and add to request.responses
    if form.is_valid():
        responses = request.session.get('responses')
        for key, value in request.POST.items():
            if key.startswith('word_'):
                cdiresult = CdiResult()
                cdiresult.subject = get_object_or_404(SubjectData, pk=run_uuid)
                cdiresult.given_label = key[5:]
                if value.lower() == 'on':
                    cdiresult.response = True
                    responses.append(bool(1))
                else:
                    cdiresult.response = False
                    responses.append(bool(0))
                cdiresult.save()

        request.session['responses'] = responses     

        irt_run = request.session.get('irt_run')
        if irt_run < experiment.num_words-1: 
            request.session['irt_run'] = irt_run + 1
            # generate subsequent item
            return cdiGenerateNextItem(request, run_uuid)      
        else: # proceed to experiment
            if experiment.recording_option == 'NON': # capture key/click responses only, skip webcam/microphone test.
                return HttpResponseRedirect(reverse('experiments:experimentRun', args=(run_uuid,)))
            else: # capture audio/video
                return HttpResponseRedirect(reverse('experiments:webcamTest', args=(run_uuid,)))
    t = Template(experiment.cdi_page_tpl)
    c = RequestContext(request, {'subject_data': subject_data, 'cdi_form':form, 'experiment': experiment,})
    return HttpResponse(t.render(c))

def cdiGenerateNextItem(request, run_uuid):
    """
    Generates subsequent test item.
    """
    subject_data = get_object_or_404(SubjectData, pk=run_uuid)
    experiment = get_object_or_404(Experiment, pk=subject_data.experiment.pk)
    
    #est_theta = estimator.estimate(items=items, administered_items=administered_items, response_vector=responses, est_theta=est_theta)
    #request.session['est_theta'] = est_theta      
    # generate subsequent items
    try:
        # estimate and update theta 
        irt_run = request.session.get('irt_run')
        item_params = request.session.get('item_params')
        item_params = pd.read_json(item_params).iloc[:, 1:5].to_numpy()
        administered_items = request.session.get('administered_items')
        responses = request.session.get('responses')
        est_theta = request.session.get('est_theta')
        est_theta = HillClimbingEstimator().estimate(items=item_params, administered_items=administered_items, response_vector=responses, est_theta=est_theta)
        request.session['est_theta'] = est_theta  
        words = request.session.get('words')
        all_words = json.loads(request.session.get('all_words'))

        logger.info('est theta: ' + str(est_theta))
        
        if np.isinf(est_theta):
            # generate IRT subsequent 'initial' items
            administered_items = sort_items(item_params)[0:1+irt_run, ].tolist()
            request.session['administered_items'] = administered_items
        else:
            # generate new items
            item_index = MaxInfoSelector().select(items=item_params, administered_items=administered_items, est_theta=est_theta)
            administered_items.append(item_index.tolist())
            request.session['administered_items'] = administered_items
        words.append(all_words[administered_items[irt_run]]) 
        request.session['words'] = words
        form = VocabularyChecklistForm(cdi_form=experiment, word=words[irt_run])
    except KeyError as e:
        logger.exception('Failed to generate cdi item: ' + str(e))
        return HttpResponseRedirect(reverse('experiments:experimentError', args=(run_uuid,)))
    else:
        t = Template(experiment.cdi_page_tpl)
        c = RequestContext(request, {'subject_data': subject_data, 'cdi_form': form, 'experiment': experiment,})
        return HttpResponse(t.render(c))
