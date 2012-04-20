import commonware.log
import jingo
from django import http
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache

from models import tutorials, MdnCache
from cron import refresh_mdn_cache

log = commonware.log.getLogger('z.ecosystem')
cache_prefix = 'ecosystem.tutorials.'

def landing_page(request):
    return jingo.render(request, 'ecosystem/landing_page.html')

def tutorial_page(request, page):

    if not page:
        page = 'apps'

    try:
        data = _get_page(page)
    except ObjectDoesNotExist:
        raise http.Http404()

    ctx = { 'tutorials': tutorials, 'page': page, 'content': data.content, 'toc': data.toc }

    return jingo.render(request, 'ecosystem/tutorial_page.html', ctx)

def _get_page(page):
    data = cache.get(cache_prefix + page)
    if data == None:        
        data = MdnCache.objects.get(name=page)
        cache.set(cache_prefix + page, data, 60 * 60 * 24)
    return data