
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


def setup_settings(settings, **kwargs):

    settings['MIDDLEWARE'] += [
        'seo.middleware.PageMetaMiddleware'
    ]


class SeoConfig(AppConfig):
    name = 'seo'
    verbose_name = _("SEO")


default_app_config = 'seo.SeoConfig'
