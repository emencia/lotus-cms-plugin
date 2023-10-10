from cms.models.pluginmodel import CMSPlugin
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from lotus.choices import STATUS_PUBLISHED, get_status_choices


USER_LANGUAGE = (("user_s_language", _("User's language")),)


PUBLIC_ONLY = (("public_only", _("Public only")),)
PRIVATE_ONLY = (("private_only", _("Private only if accessible")),)
PUBLIC_AND_PRIVATE = (("public_and_private", _("Public and private if accessible")),)


def get_lotus_plugin_template_default():
    return settings.BLOCKS_LOTUS_PLUGIN_TEMPLATES[0][0]


def get_lotus_plugin_template_choices():
    return settings.BLOCKS_LOTUS_PLUGIN_TEMPLATES


class ArticlePluginParams(CMSPlugin):
    title = models.CharField(
        verbose_name=_("Plugin title"),
        max_length=50,
        default=_("Articles"),
    )
    cards_quantity = models.IntegerField(
        default=5,
        validators=[MinValueValidator(3)],
        verbose_name=_("Article quantity to display"),
    )
    categories = models.ManyToManyField(
        "lotus.Category",
        verbose_name=_("Display articles related to following categories"),
        blank=True,
        help_text=_("Leave blank to avoid filtering by any category"),
    )
    status = models.SmallIntegerField(
        verbose_name=_("Display articles with following status"),
        choices=get_status_choices(),
        default=STATUS_PUBLISHED,
        blank=True,
        null=True,
    )

    privacy_criterion = models.CharField(
        default=PUBLIC_ONLY[0][0],
        choices=PRIVATE_ONLY + PUBLIC_AND_PRIVATE + PUBLIC_ONLY,
        max_length=128,
        verbose_name=_("Select a privacy criterion"),
    )
    featured = models.BooleanField(
        default=False,
        verbose_name=_("Display only featured articles"),
        help_text=_("Display only articles with 'featured' set to True.")
    )
    tags = models.ManyToManyField(
        "taggit.Tag",
        verbose_name=_("Display articles related to following tags"),
        blank=True,
        help_text=_("Leave blank to avoid filtering by any tag"),
    )
    template = models.CharField(
        _("Template"),
        blank=False,
        max_length=150,
        choices=get_lotus_plugin_template_choices(),
        default=get_lotus_plugin_template_default(),
        help_text=_("Used template for content formatting."),
    )

    def copy_relations(self, oldinstance):
        """
        Handle copying of any relations attached to this plugin.

        This method takes an old instance of the ArticlePluginParams and copies its
        relations (tags and categories) to the current instance.

        Args:
            oldinstance (ArticlePluginParams): instance from which to copy foreigns
            relations.

        Returns:
            None
        """
        self.tags.set(oldinstance.tags.all())
        self.categories.set(oldinstance.categories.all())
