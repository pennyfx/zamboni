import urllib2
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache

import lxml
from lxml import html, etree

from models import tutorials, MdnCache
import commonware.log

log = commonware.log.getLogger('z.ecosystem.cron')
cache_prefix = 'ecosystem.tutorials.'


def refresh_mdn_cache():

    MdnCache.objects.all().delete()

    for item in tutorials:
        try:
            content = _fetch_mdn_page(item)        
        except Exception as e:
            log.error('Failed fetching Mdn Item "%s" reason: %s' % (item['name'], e))
            continue
        
        model = MdnCache.objects.create(name=item['name'])
        model.title = item['title']
        model.toc = content[0]
        model.content = content[1]
        model.permalink = item['mdn']
        model.modified = datetime.now()
        model.save()
        
        cache.delete(cache_prefix + item['name'])


def _fetch_mdn_page(item):

    response = urllib2.urlopen(item['mdn'])
    root = lxml.html.fromstring(response.read())
    
    toc = root.cssselect('#article-nav div.page-toc ol')[0]
    content = root.cssselect('#pageText')[0]

    toc.set('id', 'mdn-toc')
    content.set('id', 'mdn-content')

    return (etree.tostring(_clean_html_tree(toc), pretty_print=True),
        etree.tostring(_clean_html_tree(content), pretty_print=True)) 


def _clean_html_tree(tree):
    
    for elem in tree.iter():
        try: 
            del elem.attrib['style']             
        except:
            pass
    return tree
   