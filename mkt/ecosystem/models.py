import os
from datetime import datetime

from django.db import models
from django.conf import settings

import amo.models

tutorials = [
        { 
            'title': 'Example Tutorial', 
            'name': 'example', 
            'mdn': 'https://developer.mozilla.org/en/HTML/HTML5' },
        { 
            'title': 'Apps Tutorial', 
            'name': 'apps', 
            'mdn': 'https://developer.mozilla.org/en/Apps/Tracks/General'  },
        { 
            'title': 'Games Tutorial', 
            'name':'games', 
            'mdn': 'https://developer.mozilla.org/en/Apps/Tracks/Games' },
        #{   
        #    'title': 'Social Tutorial', 
        #    'name': 'social', 
        #    'mdn': 'https://developer.mozilla.org/en/Apps/Tracks/Social' },
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
