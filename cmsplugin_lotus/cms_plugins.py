from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.db import models
from django.forms import CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _
from cmsplugin_lotus.models import (
    ArticlePluginParams,
    get_lotus_plugin_template_default
)
from cmsplugin_lotus.queryset_maker import ArticleQuerySetMaker
from cmsplugin_lotus.utils.privacy_filters import apply_privacy_filter


def filter_article_params(context, instance):
    """
    Filter articles based on plugin parameters and request.

    This function applies privacy filters on the articles based on the plugin parameters
    and current request.
    It uses the `_apply_privacy_filter` function to set the filters.

    Args:
        context (dict): The current context, must include 'request'.
        instance (ArticlePluginParams): An instance of the plugin parameters.

    Returns:
        ArticleQuerySetMaker or EmptyQuerySet of Article: The updated
        ArticleQuerySetMaker object with applied filters or an EmptyQuerySet object.
    """
    request = context["request"]
    article_filter = ArticleQuerySetMaker.from_plugin_params(instance)
    return apply_privacy_filter(instance, request, article_filter)


class LatestArticlesPlugin(CMSPluginBase):
    model = ArticlePluginParams
    name = _("Latest Article Plugin")
    render_template = get_lotus_plugin_template_default()
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    cache = False  # We are using context object.

    def render(self, context, instance, placeholder):
        """Render the latest articles in the context.

        This method takes the current context, instance of the plugin, and placeholder
        to update the context with filtered articles.
        It uses the `filter_article_params` function to get the filtered articles and
        then updates the context.

        Args:
            context (dict): The current context.
            instance (ArticlePluginParams): An instance of the plugin parameters.
            placeholder (Placeholder): The placeholder where the plugin resides.

        Returns:
            dict: The updated context with filtered articles.
        """
        context = super().render(context, instance, placeholder)
        self.render_template = instance.template
        article_filter = filter_article_params(context, instance)
        context.update(
            {
                "articles": article_filter(),
                "instance": instance,
            }
        )
        return context


plugin_pool.register_plugin(LatestArticlesPlugin)
