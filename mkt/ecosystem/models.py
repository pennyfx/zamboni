import os
from datetime import datetime
from django.db import models
from django.conf import settings
import amo.models


#TODO: move to settings 
mdnUrl = 'https://developer.mozilla.org/en'

tutorials = [
        { 
            'title': 'Example Tutorial', 
            'name': 'example', 'mdn': '%s/HTML/HTML5' % mdnUrl },
        { 
            'title': 'Apps Tutorial', 
            'name': 'apps', 'mdn': '%s/Apps/Tracks/General' % mdnUrl },
        { 
            'title': 'Games Tutorial', 
            'name':'games', 'mdn': '%s/Apps/Tracks/Games' % mdnUrl },
        #{   
        #    'title': 'Social Tutorial', 
        #    'name': 'social', 'mdn': '%s/Apps/Tracks/Social' % mdnUrl },
]

class MdnCache(models.Model):

    name = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255, default='', blank=True)    
    toc = models.TextField(blank=True)
    content = models.TextField(blank=True)
    permalink = models.CharField(max_length=255, default='', blank=True)
    modifed = models.DateTimeField(default=datetime.now, blank=True)    

    class Meta:
        db_table = 'mdn_cache'

    def __unicode__(self):
        return self.title