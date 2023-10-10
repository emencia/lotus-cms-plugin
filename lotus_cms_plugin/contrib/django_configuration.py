from ..defaults import BLOCKS_LOTUS_PLUGIN_TEMPLATES


class LotusCmsPluginDefaultSettings:
    """
    Default application settings class to use with a "django-configuration" class.

    Example:

        You just have to inherit from it in your settings class: ::

            from configurations import Configuration
            from lotus_cms_plugin.contrib.django_configuration import LotusCmsPluginDefaultSettings

            class Dev(LotusCmsPluginDefaultSettings, Configuration):
                DEBUG = True

                BLOCKS_LOTUS_PLUGIN_TEMPLATES = [
                    ("lotus_cms_plugin/latest_articles/default.html", "Default"),
                    ("path/to/custom/template", "A custom template"),
                ]

        This will override only the setting ``BLOCKS_LOTUS_PLUGIN_TEMPLATES``, all other
        application settings will have the default values from
        ``lotus_cms_plugin.defaults``.
    """  # noqa: E501
    BLOCKS_LOTUS_PLUGIN_TEMPLATES = BLOCKS_LOTUS_PLUGIN_TEMPLATES
