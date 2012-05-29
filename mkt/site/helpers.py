import json

from jingo import register, env
import jinja2
from tower import ugettext as _
import waffle

from amo.helpers import urlparams
from amo.urlresolvers import reverse
from amo.utils import JSONEncoder
from translations.helpers import truncate


def new_context(context, **kw):
    c = dict(context.items())
    c.update(kw)
    return c


@register.function
def no_results():
    # This prints a "No results found" message. That's all. Carry on.
    t = env.get_template('site/helpers/no_results.html').render()
    return jinja2.Markup(t)


@jinja2.contextfunction
@register.function
def market_button(context, product):
    request = context['request']
    if product.is_webapp():
        faked_purchase = False
        purchased = (request.amo_user and
                     product.pk in request.amo_user.purchase_ids())
        # App authors are able to install their apps free of charge.
        if (not purchased and
            request.check_ownership(product, require_author=True)):
            purchased = faked_purchase = True
        classes = ['button', 'product']
        label = product.get_price()
        product_dict = product_as_dict(request, product, purchased=purchased)
        data_attrs = {
            'product': json.dumps(product_dict, cls=JSONEncoder),
            'manifestUrl': product.manifest_url
        }
        if product.is_premium() and product.premium:
            classes.append('premium')
        if not product.is_premium() or purchased:
            classes.append('install')
            label = _('Install')
        c = dict(product=product, label=label, purchased=purchased,
                 faked_purchase=faked_purchase, data_attrs=data_attrs,
                 classes=' '.join(classes))
        t = env.get_template('site/helpers/webapp_button.html')
    return jinja2.Markup(t.render(c))


def product_as_dict(request, product, purchased=None):

    # Dev environments might not have authors set.
    author = ''
    author_url = ''
    if product.listed_authors:
        author = product.listed_authors[0].name
        author_url = product.listed_authors[0].get_url_path()

    ret = {
        'id': product.id,
        'name': product.name,
        'manifestUrl': product.manifest_url,
        'preapprovalUrl': reverse('detail.purchase.preapproval',
                                  args=[product.app_slug]),
        'recordUrl': urlparams(product.get_detail_url('record'),
                               src=request.GET.get('src', '')),
        'author': author,
        'author_url': author_url,
        'iconUrl': product.get_icon_url(64)
    }
    if product.is_premium() and product.premium:
        ret.update({
            'price': product.premium.get_price() or '0',
            'priceLocale': product.premium.get_price_locale(),
            'purchase': product.get_purchase_url(),
        })
        currencies = product.premium.supported_currencies()
        if len(currencies) > 1 and waffle.switch_is_active('currencies'):
            currencies_dict = dict([(k, v.get_price_locale())
                                    for k, v in currencies])
            ret['currencies'] = json.dumps(currencies_dict, cls=JSONEncoder)
        if request.amo_user:
            ret['isPurchased'] = purchased
    # Jinja2 escape everything except this whitelist so that bool is retained
    # for the JSON encoding.
    wl = ('isPurchased', 'price', 'currencies')
    return dict([k, jinja2.escape(v) if k not in wl else v]
                for k, v in ret.items())


@register.filter
@jinja2.contextfilter
def promo_slider(context, products, feature=False):
    c = {
        'products': products,
        'feature': feature,
    }
    t = env.get_template('site/promo_slider.html')
    return jinja2.Markup(t.render(c))


@register.function
@jinja2.contextfunction
def mkt_breadcrumbs(context, product=None, items=None, crumb_size=40,
                    add_default=True, cls=None):
    """
    Wrapper function for ``breadcrumbs``.

    **items**
        list of [(url, label)] to be inserted after Add-on.
    **product**
        Adds the App/Add-on name to the end of the trail.  If items are
        specified then the App/Add-on will be linked.
    **add_default**
        Prepends trail back to home when True.  Default is False.
    """
    if add_default:
        crumbs = [(reverse('home'), _('Home'))]
    else:
        crumbs = []

    if product:
        if items:
            url_ = product.get_detail_url()
        else:
            # The Product is the end of the trail.
            url_ = None
        crumbs += [(reverse('browse.apps'), _('Apps')),
                   (url_, product.name)]
    if items:
        crumbs.extend(items)

    if len(crumbs) == 1:
        crumbs = []

    crumbs = [(url_, truncate(label, crumb_size)) for (url_, label) in crumbs]
    t = env.get_template('site/helpers/breadcrumbs.html').render(
        breadcrumbs=crumbs, cls=cls)
    return jinja2.Markup(t)


@register.function
def form_field(field, label=None, tag='div', req=None, opt=False, hint=False,
               some_html=False, cc_startswith=None, cc_for=None,
               cc_maxlength=None, grid=False, **attrs):
    c = dict(field=field, label=label or field.label, tag=tag, req=req,
             opt=opt, hint=hint, some_html=some_html,
             cc_startswith=cc_startswith, cc_for=cc_for,
             cc_maxlength=cc_maxlength, grid=grid, attrs=attrs)
    t = env.get_template('site/helpers/simple_field.html').render(**c)
    return jinja2.Markup(t)


@register.function
def grid_field(field, label=None, tag='div', req=None, opt=False, hint=False,
               some_html=False, cc_startswith=None, cc_maxlength=None,
               **attrs):
    return form_field(field, label, tag, req, opt, hint, some_html,
                      cc_startswith, cc_maxlength, grid=True, attrs=attrs)


@register.filter
@jinja2.contextfilter
def timelabel(context, time):
    t = env.get_template('site/helpers/timelabel.html').render(time=time)
    return jinja2.Markup(t)


@register.function
def admin_site_links():
    return {
        'addons': [
            ('Search for apps by name or id', reverse('zadmin.addon-search')),
            ('Featured add-ons', reverse('admin.featured_apps')),
            ('Name blocklist', reverse('zadmin.addon-name-blocklist')),
            ('Fake mail', reverse('zadmin.mail')),
            ('Flagged reviews', reverse('zadmin.flagged')),
        ],
        'users': [
            ('Configure groups', reverse('admin:access_group_changelist')),
        ],
        'settings': [
            ('View site settings', reverse('zadmin.settings')),
            ('Django admin pages', reverse('zadmin.home')),
            ('Site Events', reverse('zadmin.site_events')),
        ],
        'tools': [
            ('View request environment', reverse('amo.env')),
            ('Manage elasticsearch', reverse('zadmin.elastic')),
            ('Manage EcoSystem', reverse('mkt.zadmin.ecosystem')),
            ('View celery stats', reverse('zadmin.celery')),
            ('Purge data from memcache', reverse('zadmin.memcache')),
            ('Purge pages from zeus', reverse('zadmin.hera')),
            ('View graphite trends', reverse('amo.graphite', args=['addons'])),
            ('Create a new OAuth Consumer',
             reverse('zadmin.oauth-consumer-create')),
            ('Generate error', reverse('zadmin.generate-error')),
            ('Site Status', reverse('amo.monitor')),
        ],
    }
