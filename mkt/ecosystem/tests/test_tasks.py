from nose.tools import eq_

import amo.tests
from mkt.ecosystem.cron import refresh_mdn_cache, _fetch_mdn_page
from mkt.models import tutorials, MdnCache

class TestMdnCacheUpdate(amo.tests.TestCase):
	def setUp():
		tutorials = [
			{ 
        'title': 'Example Tutorial', 
        'name': 'test', 'mdn': 'https://developer.mozilla.org/en/HTML/HTML5' }
		  ]

  def test_get_page_content():
    content = _fetch_mdn_page(tutorials[0])
    _eql(2, len(content))

  def test_refresh_mdn_cache():
    _eql(0, len(MdnCache.objects.count())
    refresh_mdn_cache()
    _eql('test', MdnCache.objects.get(name=tutorials[0]['name']).name)
