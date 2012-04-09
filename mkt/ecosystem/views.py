import commonware.log
import jingo

log = commonware.log.getLogger('z.ecosystem')

def landing_page(request):
    return jingo.render(request, 'ecosystem/landing_page.html')

def content_page(request):
    return jingo.render(request, 'ecosystem/landing_page.html')
